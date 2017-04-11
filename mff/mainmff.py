import base64

import imghdr
import multiprocessing
import os
import threading
import time
import jsonpickle
from PIL import Image
import uuid
from wand.image import Image as WImage

from werkzeug.utils import secure_filename
from mff.mffhelper import get_char_json

UPLOAD_FOLDER = '/var/www/app_dancmc/mff/uploaded_screenshots'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']

def do_ocr(file_list):
    timer = time.time()

    class ResultJSON:
        def __init__(self):
            self.time_taken = 0
            self.number_total_files = 0
            self.number_invalid_files = 0
            self.successful = list()
            self.failures = list()
            self.duplicate_gears = list()

    result_json = ResultJSON()
    num_total_files = len(file_list)
    num_invalid_images = 0

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

    def log_result(result):
        print(result)
        if result is None:
            nonlocal num_invalid_images
            num_invalid_images += 1
        # Add resized thumbnails to failures
        elif type(result) is str:
            result_json.failures.append(resize_and_to_base64(result))
        # Add resized thumbnails and json to successful
        elif len(result) == 2:
            print(result["result_json"])
            result_json.successful.append({resize_and_to_base64(result["filepath"]): result["result_json"]})
        # Add resized thumbnails and json to duplicate gears
        elif len(result) == 3:
            char_list = result["char_list"]
            char_dict = {}
            for char in char_list:
                char_dict[char["char_alias"]] = char["gear_num"]

            result_json.duplicate_gears.append(
                {"thumbnail_base64": resize_and_to_base64(result['filepath']),
                 "gear_name": result['char_list'][0]["gear_name"],
                 "gear_json": result["gear_json"],
                 "char_list": char_dict}
            )

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

        result_json.time_taken = time_taken
        result_json.number_total_files = num_total_files
        result_json.number_invalid_files = num_invalid_images

        final = jsonpickle.encode(result_json, unpicklable=False)
        return final

    # request.files returns an immutable multidict
    ## request.files['file'] only retrieves the first value
    # if 'file' not in request.files:
    #     # reroutes as a get request
    #     print("file not in request.files")
    #     return redirect(request.url)

    # validate file as image
    def get_ext(file):
        # remember to return read cursor to start
        ext = imghdr.what("", file.read())
        file.seek(0)
        ext = None if ext is None else ext.lower()
        return ext if ext in ALLOWED_EXTENSIONS else None

    # remove all non-valid files
    for file in file_list:
        if file and file.filename != '':
            ext = get_ext(file)
            print(ext)
            if ext is None:
                file_list.remove(file)
                num_invalid_images += 1
            else:
                file.filename = str(int(time.time())) + "_" + str(uuid.uuid4().time_low) + "." + ext

    #
    file_paths = list()
    if not os.path.isdir(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    for file in file_list:
        file_path =UPLOAD_FOLDER+"/" +secure_filename(file.filename)
        # file.save(file_path)

        with WImage(file=file, resolution=600) as image:
            image.compression_quality = 95
            image.save(filename=file_path)
        file_paths.append(file_path)

    # pass on
    return process_images(validated_file_paths=file_paths)

