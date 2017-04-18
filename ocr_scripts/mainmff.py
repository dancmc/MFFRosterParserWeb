import base64
import imghdr
import multiprocessing
import os
import threading
import time
import uuid
from flask import g

from . import databasehelper as db
import jsonpickle
from PIL import Image
from werkzeug.utils import secure_filename

from .mffhelper import UnsupportedRatioException
from .mffhelper import get_char_json

UPLOAD_FOLDER = '/var/www/app_dancmc/mff/ocr_scripts/uploaded_screenshots'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']


def do_ocr(file_list, request_mode):
    timer = time.time()

    class ResultJSON:
        def __init__(self):
            self.time_taken = 0
            self.number_total_files = 0
            self.number_invalid_files = 0
            self.successful = list()
            self.failures = list()
            self.duplicate_gears = list()

    multi_final_json = ResultJSON()
    single_final_json = {"success": False,
                         "error": 4}
    num_total_files = len(file_list)
    num_invalid_images = 0

    sql_count = 0
    sql_data_tuple = ()

    def delete_file(filepath):
        time.sleep(3)
        try:
            os.remove(filepath)
        except:
            time.sleep(5)
            try:
                os.remove(filepath)
            except:
                pass

    def resize_and_to_base64(filepath):
        folder, file = os.path.split(filepath)
        filename, ext = os.path.splitext(file)

        image = Image.open(filepath)

        # targeting thumbnail width of 450
        original_w = image.size[0]
        original_h = image.size[1]
        print(original_w)
        scale = 500 / original_w

        # modifies image object in place
        image.thumbnail((int(original_w * scale), int(original_h * scale)))
        thumbnail_path = os.path.join(UPLOAD_FOLDER, filename + "_small" + ext)
        image.save(thumbnail_path, "JPEG")

        image = open(thumbnail_path, 'rb')
        image_read = image.read()
        image_dataurl = 'data:image/jpg;base64,' + (str(base64.b64encode(image_read)).strip("'")[2:])

        thread = threading.Thread(target=delete_file, args=(thumbnail_path,))
        thread.start()
        # os.remove(thumbnail_path)
        return image_dataurl

    def generate_sql(char_alias=None, uni_alias=None, tier=None, phys_att=None,
                     energy_att=None, atk_spd=None, crit_rate=None, crit_dam=None,
                     def_pen=None, ignore_dodge=None, phys_def=None, energy_def=None,
                     hp=None, reco_rate=None, dodge=None, mv_spd=None, debuff=None,
                     scd=None, gear_name=None, type_1=None, val_1=None, type_2=None,
                     val_2=None, type_3=None, val_3=None, type_4=None, val_4=None,
                     type_5=None, val_5=None, type_6=None, val_6=None, type_7=None,
                     val_7=None, type_8=None, val_8=None, filename=None, time_utc=None):

        nonlocal sql_count
        sql_count += 1
        nonlocal sql_data_tuple
        sql_data_tuple += (char_alias, uni_alias, tier, phys_att, energy_att, atk_spd, crit_rate, crit_dam,
                           def_pen, ignore_dodge, phys_def, energy_def, hp, reco_rate, dodge, mv_spd, debuff,
                           scd, gear_name, type_1, val_1, type_2, val_2, type_3, val_3, type_4, val_4,
                           type_5, val_5, type_6, val_6, type_7, val_7, type_8, val_8, filename, time_utc)

    def log_result(result):
        # print(result)

        nonlocal num_invalid_images
        nonlocal single_final_json
        nonlocal multi_final_json

        # Failed - invalid file format
        if result is None:
            # results
            num_invalid_images += 1

            single_final_json = {"success": False,
                                 "error": 1}

            # sql logs
            generate_sql()


        # Failed - Unsupported ratio
        elif result is UnsupportedRatioException:
            # results
            num_invalid_images += 1

            single_final_json = {"success": False,
                                 "error": 3}

            # sql logs
            generate_sql()

        # Failed - wrong screenshot page/OCR failed
        elif type(result) is str:
            # results
            if request_mode == "multi":
                multi_final_json.failures.append(resize_and_to_base64(result))

            single_final_json = {"success": False,
                                 "error": 2}

            # sql logs
            generate_sql(filename=os.path.split(result)[1], time_utc=int(time.time()))


        # Successful - details
        elif result["type"] == "details":

            char = result["result_char"]

            if request_mode == "multi":
                result_json = '"' + char.id + '":' + jsonpickle.encode(char, unpicklable=False)
                multi_final_json.successful.append({resize_and_to_base64(result["filepath"]): result_json})

            single_final_json = {"success": True,
                                 "type": "details",
                                 "content": {"id": char.id, "uniform": char.uniform, "tier": char.tier,
                                             "phys_att": char.attack.physical, "energy_att": char.attack.energy,
                                             "atkspeed": char.atkspeed, "crit_rate": char.critrate,
                                             "critdamage": char.critdamage, "defpen": char.defpen,
                                             "ignore_dodge": char.ignore_dodge, "phys_def": char.defense.physical,
                                             "energy_def": char.defense.energy, "hp": char.hp,
                                             "recorate": char.recorate, "dodge": char.dodge,
                                             "movspeed": char.movspeed, "debuff": char.debuff,
                                             "scd": char.scd}}

            # sql logs
            generate_sql(filename=os.path.split(result["filepath"])[1], char_alias=char.id, uni_alias=char.uniform,
                         tier=char.tier, phys_att=char.attack.physical, energy_att=char.attack.energy,
                         atk_spd=char.atkspeed, crit_rate=char.critrate, crit_dam=char.critdamage,
                         def_pen=char.defpen, ignore_dodge=char.ignore_dodge, phys_def=char.defense.physical,
                         energy_def=char.defense.energy, hp=char.hp, reco_rate=char.recorate, dodge=char.dodge,
                         mv_spd=char.movspeed, debuff=char.debuff, scd=char.scd, time_utc=int(time.time()))


        # Successful - single gear
        elif result["type"] == "gear":
            char_list = result["char_list"]
            char_dict = {}
            for char in char_list:
                char_dict[char["id"]] = char["gear_num"]


            char = result["result_char"]
            if request_mode == "multi":
                result_json = '"' + char.id + '":' + jsonpickle.encode(char, unpicklable=False)
                multi_final_json.successful.append({resize_and_to_base64(result["filepath"]): result_json})

            gear = char.gear[result["gear_num"]-1]
            single_final_json = {"success":True,
                                 "type":"gear",
                                 "content": {"char_list": char_dict,
                                             "gear_val": gear}}
            # sql logs
            generate_sql(filename=os.path.split(result["filepath"])[1], char_alias=char.id, type_1=gear[0].type,
                         val_1=gear[0].val, type_2=gear[1].type, val_2=gear[1].val, type_3=gear[2].type,
                         val_3=gear[2].val, type_4=gear[3].type, val_4=gear[3].val, type_5=gear[4].type,
                         val_5=gear[4].val, type_6=gear[5].type, val_6=gear[5].val, type_7=gear[6].type,
                         val_7=gear[6].val, type_8=gear[7].type, val_8=gear[7].val,
                         gear_name=result["gear_name"], time_utc=int(time.time()))


        # Successful - dup gears
        elif result["type"] == "gear_dup":
            char_list = result["char_list"]
            char_dict = {}
            for char in char_list:
                char_dict[char["id"]] = char["gear_num"]

            gear = result["gear"]
            gear_json = jsonpickle.encode(gear, unpicklable=False)

            if request_mode == "multi":
                multi_final_json.duplicate_gears.append(
                    {"thumbnail_base64": resize_and_to_base64(result['filepath']),
                     "gear_name": result['char_list'][0]["gear_name"],
                     "gear_json": gear_json,
                     "char_list": char_dict}
                )

            single_final_json = {"success": True,
                                 "type": "gear",
                                 "content": {"char_list": char_dict,
                                             "gear_val": gear}}

            # sql logs
            generate_sql(time_utc=int(time.time()), filename=os.path.split(result["filepath"])[1],
                         gear_name=result['char_list'][0]["gear_name"], type_1=gear[0].type,
                         val_1=gear[0].val, type_2=gear[1].type, val_2=gear[1].val, type_3=gear[2].type,
                         val_3=gear[2].val, type_4=gear[3].type, val_4=gear[3].val, type_5=gear[4].type,
                         val_5=gear[4].val, type_6=gear[5].type, val_6=gear[5].val, type_7=gear[6].type,
                         val_7=gear[6].val, type_8=gear[7].type, val_8=gear[7].val)

    def process_images(validated_file_paths):

        # Processing single file takes 0.2-0.5 secs, mp overhead only worth it >3
        if len(validated_file_paths) > 3:
            pool = multiprocessing.Pool(processes=None)
            for i in validated_file_paths:
                pool.apply_async(get_char_json, args=(i,), callback=log_result)
            pool.close()
            pool.join()
        else:
            for i in validated_file_paths:
                log_result(get_char_json(i))

        time_taken = str(time.time() - timer)
        print("Time taken ; "+time_taken)

        multi_final_json.time_taken = time_taken
        multi_final_json.number_total_files = num_total_files
        multi_final_json.number_invalid_files = num_invalid_images

        final = ""
        if(request_mode=="single"):
            final= jsonpickle.encode(single_final_json, unpicklable=False)
        if(request_mode=="multi"):
            final = jsonpickle.encode(multi_final_json, unpicklable=False)

        sql_statement = "INSERT INTO log (char_alias, uni_alias, tier, phys_att, energy_att, atk_spd, crit_rate, crit_dam," \
                        "def_pen, ignore_dodge, phys_def, energy_def, hp, reco_rate, dodge, mv_spd, debuff," \
                        "scd, gear_name, type_1, val_1, type_2, val_2, type_3, val_3, type_4, val_4," \
                        "type_5, val_5, type_6, val_6, type_7, val_7, type_8, val_8, filename, time_utc) " \
                        "VALUES "

        values_list = ['(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)']*sql_count
        sql_statement = sql_statement + ",".join(values_list) + ";"

        try:
            db.insert_log(sql_statement, sql_data_tuple)
        except:
            pass

        return final



    # validate file as image
    def get_ext(file):
        # remember to return read cursor to start
        ext = imghdr.what("", file.read())
        file.seek(0)
        ext = None if ext is None else ext.lower()
        return ext if ext in ALLOWED_EXTENSIONS else None

    # remove all non-valid files
    for file in file_list:

        # if file:
        ext = get_ext(file)
        print(ext)
        if ext is None:
            file_list.remove(file)
            num_invalid_images += 1

            if request_mode=="single":
                return jsonpickle.encode({"success": False, "error": 1}, unpicklable=False)
        else:
            file.filename = str(int(time.time())) + "_" + str(uuid.uuid4().time_low) + "." + ext
        # else :
        #     return jsonpickle.encode({"success": False, "error": 1}, unpicklable=False)

    #
    file_paths = list()
    if not os.path.isdir(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    for file in file_list:
        file_path = UPLOAD_FOLDER + "/" + secure_filename(file.filename)
        file.save(file_path)

        # with WImage(file=file, resolution=600) as image:
        #     image.compression_quality = 95
        #     image.save(filename=file_path)
        file_paths.append(file_path)

    # pass on
    return process_images(validated_file_paths=file_paths)
