import datetime

import Levenshtein
import jsonpickle
from PIL import Image
from mff.databasehelper import *
from mff.ocr import Ocr
import math


ASPECT_RATIO_16_9 = 1.777777
ASPECT_RATIO_16_10 = 1.6
ASPECT_RATIO_4_3 = 1.3333333
ASPECT_RATIO_185_9 = 2.055555
ASPECT_RATIO_15_10 = 1.5


class UnsupportedRatioException(ValueError):
    pass


ocr_ob = Ocr()


class Rects:
    def __init__(self, width: int, height: int):

        aspect = width / height
        scale = 1.


        def scale_rect(rect):
            return tuple(int(scale * i) for i in rect)

        if math.isclose(ASPECT_RATIO_16_9, aspect, rel_tol=0.04):
            scale = width / 1920
            print(scale)

            self.rect_check_details_page = scale_rect((586, 184, 733, 223))
            self.rect_check_gear_page = scale_rect((156, 23, 313, 74))
            self.rect_gear_name = scale_rect((387, 143, 1018, 187))

            self.rect_tier = scale_rect((460, 393, 555, 427))
            self.rect_char = scale_rect((104, 479, 546, 520))
            self.rect_uni = scale_rect((108, 523, 554, 560))
            self.rect_phys_att = scale_rect((893, 240, 1186, 280))
            self.rect_energy_att = scale_rect((893, 280, 1186, 327))
            self.rect_atk_spd = scale_rect((893, 327, 1186, 374))
            self.rect_crit_rate = scale_rect((893, 374, 1186, 423))
            self.rect_crit_dam = scale_rect((893, 423, 1186, 468))
            self.rect_def_pen = scale_rect((893, 468, 1186, 517))
            self.rect_ignore_dodge = scale_rect((893, 517, 1186, 568))
            self.rect_phys_def = scale_rect((1499, 238, 1816, 280))
            self.rect_energy_def = scale_rect((1499, 280, 1816, 329))
            self.rect_hp = scale_rect((1499, 329, 1816, 376))
            self.rect_recorate = scale_rect((1499, 376, 1816, 421))
            self.rect_dodge = scale_rect((1499, 421, 1816, 472))
            self.rect_mv_spd = scale_rect((1541, 810, 1814, 847))
            self.rect_debuff = scale_rect((1653, 856, 1816, 895))
            self.rect_scd = scale_rect((1666, 903, 1816, 937))

            self.list_rect_gearstat = list()
            self.list_rect_gearstat.append(scale_rect((400, 304, 1024, 349)))
            self.list_rect_gearstat.append(scale_rect((400, 348, 1024, 384)))
            self.list_rect_gearstat.append(scale_rect((400, 390, 1024, 432)))
            self.list_rect_gearstat.append(scale_rect((400, 434, 1024, 475)))
            self.list_rect_gearstat.append(scale_rect((400, 477, 1024, 517)))
            self.list_rect_gearstat.append(scale_rect((400, 521, 1024, 559)))
            self.list_rect_gearstat.append(scale_rect((400, 564, 1024, 603)))
            self.list_rect_gearstat.append(scale_rect((400, 606, 1024, 646)))

        elif math.isclose(ASPECT_RATIO_16_10, aspect, rel_tol=0.04):
            scale = width / 1600
            print(scale)

            self.rect_check_details_page = scale_rect((469, 183, 588, 215))
            self.rect_check_gear_page = scale_rect((143, 15, 274, 67))
            self.rect_gear_name = scale_rect((285, 147, 859, 186))

            self.rect_tier = scale_rect((352, 367, 442, 400))
            self.rect_char = scale_rect((41, 446, 441, 482))
            self.rect_uni = scale_rect((41, 482, 441, 520))
            self.rect_phys_att = scale_rect((736, 230, 1000, 268))
            self.rect_energy_att = scale_rect((736, 268, 1000, 313))
            self.rect_atk_spd = scale_rect((736, 313, 1000, 354))
            self.rect_crit_rate = scale_rect((736, 354, 1000, 396))
            self.rect_crit_dam = scale_rect((736, 396, 1000, 437))
            self.rect_def_pen = scale_rect((736, 437, 1000, 482))
            self.rect_ignore_dodge = scale_rect((736, 482, 1000, 522))
            self.rect_phys_def = scale_rect((1278, 231, 1560, 271))
            self.rect_energy_def = scale_rect((1278, 271, 1560, 313))
            self.rect_hp = scale_rect((1278, 313, 1560, 354))
            self.rect_recorate = scale_rect((1278, 354, 1560, 397))
            self.rect_dodge = scale_rect((1278, 397, 1560, 439))
            self.rect_mv_spd = scale_rect((1299, 738, 1560, 778))
            self.rect_debuff = scale_rect((1367, 778, 1560, 817))
            self.rect_scd = scale_rect((1367, 817, 1560, 860))

            self.list_rect_gearstat = list()
            self.list_rect_gearstat.append(scale_rect((300, 290, 859, 325)))
            self.list_rect_gearstat.append(scale_rect((300, 325, 859, 365)))
            self.list_rect_gearstat.append(scale_rect((300, 365, 859, 405)))
            self.list_rect_gearstat.append(scale_rect((300, 405, 859, 443)))
            self.list_rect_gearstat.append(scale_rect((300, 443, 859, 479)))
            self.list_rect_gearstat.append(scale_rect((300, 479, 859, 518)))
            self.list_rect_gearstat.append(scale_rect((300, 518, 859, 556)))
            self.list_rect_gearstat.append(scale_rect((300, 556, 859, 596)))

        elif math.isclose(ASPECT_RATIO_4_3, aspect, rel_tol=0.04):
            scale = width / 1778
            print(scale)

            self.rect_check_details_page = scale_rect((520, 316, 655, 355))
            self.rect_check_gear_page = scale_rect((158, 16, 298, 77))
            self.rect_gear_name = scale_rect((325, 273, 960, 320))

            self.rect_tier = scale_rect((395, 515, 490, 555))
            self.rect_char = scale_rect((43, 604, 489, 647))
            self.rect_uni = scale_rect((43, 647, 490, 683))
            self.rect_phys_att = scale_rect((812, 368, 1113, 411))
            self.rect_energy_att = scale_rect((812, 411, 1113, 459))
            self.rect_atk_spd = scale_rect((812, 459, 1113, 506))
            self.rect_crit_rate = scale_rect((812, 506, 1113, 553))
            self.rect_crit_dam = scale_rect((812, 553, 1113, 597))
            self.rect_def_pen = scale_rect((812, 597, 1113, 645))
            self.rect_ignore_dodge = scale_rect((812, 645, 1113, 691))
            self.rect_phys_def = scale_rect((1419, 369, 1736, 412))
            self.rect_energy_def = scale_rect((1419, 412, 1736, 458))
            self.rect_hp = scale_rect((1419, 458, 1736, 504))
            self.rect_recorate = scale_rect((1419, 504, 1736, 552))
            self.rect_dodge = scale_rect((1419, 552, 1736, 602))
            self.rect_mv_spd = scale_rect((1434, 931, 1736, 977))
            self.rect_debuff = scale_rect((1501, 977, 1736, 1022))
            self.rect_scd = scale_rect((1501, 1022, 1736, 1066))

            self.list_rect_gearstat = list()
            self.list_rect_gearstat.append(scale_rect((337, 434, 959, 474)))
            self.list_rect_gearstat.append(scale_rect((337, 474, 959, 518)))
            self.list_rect_gearstat.append(scale_rect((337, 518, 959, 560)))
            self.list_rect_gearstat.append(scale_rect((337, 560, 959, 602)))
            self.list_rect_gearstat.append(scale_rect((337, 602, 959, 646)))
            self.list_rect_gearstat.append(scale_rect((337, 646, 959, 686)))
            self.list_rect_gearstat.append(scale_rect((337, 686, 959, 730)))
            self.list_rect_gearstat.append(scale_rect((337, 730, 959, 772)))

        elif math.isclose(ASPECT_RATIO_185_9, aspect, rel_tol=0.04):
            scale = width / 1776
            print(scale)

            self.rect_check_details_page = scale_rect((590, 146, 698, 176))
            self.rect_check_gear_page = scale_rect((127, 17, 248, 58))
            self.rect_gear_name = scale_rect((427, 114, 948, 155))

            self.rect_tier = scale_rect((487, 314, 564, 343))
            self.rect_char = scale_rect((202, 384, 564, 416))
            self.rect_uni = scale_rect((202, 416, 564, 447))
            self.rect_phys_att = scale_rect((829, 190, 1069, 224))
            self.rect_energy_att = scale_rect((829, 224, 1069, 263))
            self.rect_atk_spd = scale_rect((829, 263, 1069, 301))
            self.rect_crit_rate = scale_rect((829, 301, 1069, 341))
            self.rect_crit_dam = scale_rect((829, 341, 1069, 377))
            self.rect_def_pen = scale_rect((829, 377, 1069, 413))
            self.rect_ignore_dodge = scale_rect((829, 413, 1069, 451))
            self.rect_phys_def = scale_rect((1325, 188, 1572, 225))
            self.rect_energy_def = scale_rect((1325, 225, 1572, 265))
            self.rect_hp = scale_rect((1325, 265, 1572, 301))
            self.rect_recorate = scale_rect((1325, 301, 1572, 339))
            self.rect_dodge = scale_rect((1325, 339, 1572, 377))
            self.rect_mv_spd = scale_rect((1339, 646, 1572, 682))
            self.rect_debuff = scale_rect((1400, 682, 1572, 720))
            self.rect_scd = scale_rect((1400, 720, 1572, 756))

            self.list_rect_gearstat = list()
            self.list_rect_gearstat.append(scale_rect((439, 243, 942, 277)))
            self.list_rect_gearstat.append(scale_rect((439, 277, 942, 310)))
            self.list_rect_gearstat.append(scale_rect((439, 310, 942, 346)))
            self.list_rect_gearstat.append(scale_rect((439, 346, 942, 379)))
            self.list_rect_gearstat.append(scale_rect((439, 379, 942, 414)))
            self.list_rect_gearstat.append(scale_rect((439, 414, 942, 447)))
            self.list_rect_gearstat.append(scale_rect((439, 447, 942, 482)))
            self.list_rect_gearstat.append(scale_rect((439, 482, 942, 520)))

        else:
            raise UnsupportedRatioException


list_gear_val = ("physical_attack_by_level",
                 "physical_attack",
                 "energy_attack_by_level",
                 "energy_attack",
                 "hp_by_level",
                 "hp",
                 "defense_penetration",
                 "critical_rate",
                 "critical_damage",
                 "skill_cooldown",
                 "attack_speed",
                 "all_attack",
                 "dodge",
                 "movement_speed",
                 "recovery_rate",
                 "physical_defense_by_level",
                 "energy_defense_by_level",
                 "physical_defense",
                 "energy_defense",
                 "all_defense")
list_gear_statname = ("physicalattackperlv.",
                      "physicalattack",
                      "energyattackperlv.",
                      "energyattack",
                      "hpperlv.",
                      "hp",
                      "ignoredefense",
                      "criticalrate",
                      "criticaldamage",
                      "skillcooldown",
                      "attackspeed",
                      "allattacks",
                      "dodge",
                      "movementspeed",
                      "recoveryrate",
                      "physicaldefenseperlv.",
                      "energydefenseperlv.",
                      "physicaldefense",
                      "energydefense",
                      "alldefenses")



class GearValue:
    def __init__(self):
        self.type = ""
        self.val = 0.
        self.pref = False


class Attack:
    def __init__(self):
        self.physical = 0
        self.energy = 0


class Defense:
    def __init__(self):
        self.physical = 0
        self.energy = 0


class Character:
    def __init__(self, char_alias=""):
        self.id = char_alias
        self.uniform = ""
        self.uniforms = {}
        self.tier = 1
        self.attack = Attack()
        self.defense = Defense()
        self.hp = 0
        self.dodge = 0.
        self.ignore_dodge = 0.
        self.defpen = 0.
        self.scd = 0.
        self.critrate = 0.
        self.critdamage = 0.
        self.atkspeed = 0.
        self.recorate = 0.
        self.movspeed = 0.
        self.debuff = 0.
        self.skills = [1, 1, 1, 1, 1]
        self.gear = [[GearValue() for i in range(8)] for j in range(4)]
        self.lastUpdate = 0


    # remove last 2 attributes from state so jsonpickler does not serialise them
    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


def greyscale_ocr(image, rect, threshold=140):
    return ocr_ob.ocr_using_greyscale(image.crop(rect), threshold)

def color_ocr_text(image, rect, color=(255, 255, 255), threshold=120, inverted_colors=False):
    return ocr_ob.ocr_using_color_similarity(image.crop(rect), color=color,threshold=threshold, inverted_colors= inverted_colors)

def color_ocr_int(image, rect, color=(255, 255, 255), threshold=120, inverted_colors=False):
    num = ocr_ob.ocr_using_color_similarity(image.crop(rect), color=color,threshold=threshold, inverted_colors= inverted_colors)
    try:
        num = int(num.replace(" ", "").replace("%", "").replace("+", "").replace('"', "4").replace("s", "5").replace("o", "0").replace("d", "0").replace("z","2").replace(".","").replace(",","").replace("'",""))
    except:
        num = 0
    return num

def color_ocr_float(image, rect, color=(255, 255, 255), threshold=120, inverted_colors=False):
    num = ocr_ob.ocr_using_color_similarity(image.crop(rect), color=color,threshold=threshold, inverted_colors= inverted_colors)
    try:
        num = float(num.replace(" ", "").replace("%", "").replace("+", "").replace('"', "4").replace("s", "5").replace("o", "0").replace("d", "0").replace("z","2").replace(",",".").replace("-",".").replace("'",""))
    except:
        num = 0.
    return num


def get_gear(screenshot, rects):

    # split gear state rectangle into left and right
    def split_gear_rect(rect):
        return ((rect[0], rect[1], int((rect[2] - rect[0]) * 0.7 + rect[0]), rect[3]),
                (rect[2] - int((rect[2] - rect[0]) * 0.3), rect[1], rect[2], rect[3]))

    def do_ocr(image, rect):
        stat_rects = split_gear_rect(rect)
        left_rect = stat_rects[0]
        right_rect = stat_rects[1]

        gear_type = ""
        raw_type = color_ocr_text(image, left_rect, color=(10, 18, 35), threshold=80, inverted_colors=True).replace(" ", "").lower()
        if raw_type != "":
            for i, item in enumerate(list_gear_statname):
                if item in raw_type:
                    gear_type = list_gear_val[i]
                    break
            if gear_type == "":
                for i, item in enumerate(list_gear_statname):
                    if Levenshtein.distance(item, raw_type) < 3:
                        gear_type = list_gear_val[i]
                        break

        val = color_ocr_text(image, right_rect, color=(10, 18, 35), inverted_colors=True)
        if val != "":
            try:
                val = float(val)
            except:
                val = 0.
        else:
            val = 0.

        return gear_type, val

    gear = [GearValue() for i in range(8)]
    for i, item in enumerate(rects):
        gear[i].type, gear[i].val = do_ocr(screenshot, rects[i])
    return gear


def get_char_json(filepath):

    screenshot = Image.open(filepath)

    now = datetime.datetime.now()
    desiredwidth = 1920
    scale = desiredwidth / screenshot.size[0]
    if screenshot.size[0]< desiredwidth:
        screenshot= screenshot.resize((desiredwidth, int(scale*screenshot.size[1])), Image.NEAREST)
    elif screenshot.size[0]>desiredwidth:
        screenshot.thumbnail((int(screenshot.size[0]*scale), int(screenshot.size[1]*scale)))
    print("scaled in "+str(datetime.datetime.now()-now))

    time = datetime.datetime.now()
    width = screenshot.size[0]
    height = screenshot.size[1]

    # define rects based on aspect ratio
    try:
        rects = Rects(width, height)
    except UnsupportedRatioException:
        return None

    if color_ocr_text(screenshot, rects.rect_check_details_page, color=(10, 18, 35), inverted_colors=True).replace(" ", "") == "attack":

        char = Character()

        char.tier = 2 if ("2" in color_ocr_text(screenshot, rects.rect_tier, (8, 20, 34), inverted_colors=True ).replace("z", "2")) else 1
        char.id = get_char_alias(color_ocr_text(screenshot, rects.rect_char, color=(10, 18, 35), inverted_colors=True))
        char.uniform = get_uniform_alias(color_ocr_text(screenshot, rects.rect_uni,color=(10, 18, 35), inverted_colors=True))

        char.attack.physical = color_ocr_int(screenshot, rects.rect_phys_att, color=(255, 255, 255))
        char.attack.energy = color_ocr_int(screenshot, rects.rect_energy_att, color=(255, 255, 255))
        char.atkspeed = color_ocr_float(screenshot, rects.rect_atk_spd, color=(255, 255, 255))
        char.critrate = color_ocr_float(screenshot, rects.rect_crit_rate, color=(255, 255, 255))
        char.critdamage = color_ocr_float(screenshot, rects.rect_crit_dam, color=(255, 255, 255))
        char.defpen = color_ocr_float(screenshot, rects.rect_def_pen, color=(255, 255, 255))
        char.ignore_dodge = color_ocr_float(screenshot, rects.rect_ignore_dodge, color=(255, 255, 255))
        char.defense.physical = color_ocr_int(screenshot, rects.rect_phys_def, color=(255, 255, 255))
        char.defense.energy = color_ocr_int(screenshot, rects.rect_energy_def, color=(255, 255, 255))
        char.hp = color_ocr_int(screenshot, rects.rect_hp, color=(255, 255, 255))
        char.recorate = color_ocr_float(screenshot, rects.rect_recorate, color=(255, 255, 255))
        char.dodge = color_ocr_float(screenshot, rects.rect_dodge, color=(255, 255, 255))
        char.movspeed = color_ocr_float(screenshot, rects.rect_mv_spd, color=(255, 255, 255))
        char.debuff = color_ocr_float(screenshot, rects.rect_debuff, color=(255, 255, 255))
        char.scd = color_ocr_float(screenshot, rects.rect_scd, color=(255, 255, 255))

        return {"result_char": char, "filepath": filepath, "gear_num":-1, "gear_name":None}

    elif color_ocr_text(screenshot, rects.rect_check_gear_page,color=(10, 18, 35), inverted_colors=True).replace(" ", "") == "gear":

        gear_name = color_ocr_text(screenshot, rects.rect_gear_name, color=(255, 255, 255))
        # returns list of dicts from DB with format (char_alias, gear_name, gear_num)
        char_list = get_chars_from_gear(gear_name)

        # if managed to match to exactly 1 character, return character json, else :
        char = Character()

        if len(char_list)==0:
           return filepath
        if len(char_list) == 1:
            char.id = char_list[0]["char_alias"]
            # database returns gear numbers 1-4, have to zero it
            gear_num = char_list[0]["gear_num"] - 1
            char.gear[gear_num] = get_gear(screenshot, rects.list_rect_gearstat)
            char.uniform = get_default_uni(char.id)

            return {"result_char": char, "filepath": filepath, "gear_num":gear_num, "gear_name":gear_name}
        else:
            # return (char_list, gear_stats_list) where gear_stats_list is a list of 8 GearValue objects
            gear_result = get_gear(screenshot, rects.list_rect_gearstat)
            return {"char_list": char_list, "gear": gear_result, "filepath": filepath}
    else:
        return filepath


if __name__ == '__main__':
    time = datetime.datetime.now()

    # print(get_char_json('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-31.png'))
    print(get_char_json('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-28-12-13-38.png'))
    # print(get_char_json('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-04-02-02-02-33.png'))
    print(get_char_json('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-31 - Copy.jpg'))
    print(datetime.datetime.now() - time)
