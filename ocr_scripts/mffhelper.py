import datetime
import math

import Levenshtein
from PIL import Image
from .databasehelper import get_char_alias, get_uniform_alias, get_chars_from_gear, get_default_uni
from .ocr import Ocr

ASPECT_RATIO_16_9 = 1.777777
ASPECT_RATIO_16_10 = 1.6
ASPECT_RATIO_4_3 = 1.3333333
ASPECT_RATIO_185_9 = 2.055555
ASPECT_RATIO_3_2 = 1.5


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

            self.rect_check_details_page = scale_rect((589, 247, 691, 286))
            self.rect_check_gear_page = scale_rect((96, 21, 222, 84))
            self.rect_gear_name = scale_rect((345, 170, 1009, 216))

            self.rect_tier = scale_rect((474, 512, 560, 552))
            self.rect_char = scale_rect((90, 418, 560, 460))
            self.rect_uni = scale_rect((92, 456, 564, 495))
            self.rect_phys_att = scale_rect((927, 303, 1198, 339))
            self.rect_energy_att = scale_rect((927, 339, 1198, 380))
            self.rect_atk_spd = scale_rect((927, 380, 1198, 418))
            self.rect_crit_rate = scale_rect((927, 418, 1198, 460))
            self.rect_crit_dam = scale_rect((927, 460, 1198, 504))
            self.rect_def_pen = scale_rect((927, 504, 1198, 541))
            self.rect_ignore_dodge = scale_rect((927, 541, 1198, 587))
            self.rect_phys_def = scale_rect((1582, 301, 1829, 337))
            self.rect_energy_def = scale_rect((1582, 337, 1829, 382))
            self.rect_hp = scale_rect((1582, 382, 1829, 420))
            self.rect_recorate = scale_rect((1582, 420, 1829, 462))
            self.rect_dodge = scale_rect((1582, 462, 1829, 504))
            self.rect_mv_spd = scale_rect((1607, 808, 1829, 848))
            self.rect_debuff = scale_rect((1691, 854, 1831, 887))
            self.rect_scd = scale_rect((1695, 892, 1833, 931))

            self.list_rect_gearstat = list()
            self.list_rect_gearstat.append(scale_rect((351, 238, 1000, 276)))
            self.list_rect_gearstat.append(scale_rect((351, 276, 1000, 320)))

            self.list_rect_gearstat.append(scale_rect((351, 324, 1000, 359)))
            self.list_rect_gearstat.append(scale_rect((351, 359, 1000, 407)))
            self.list_rect_gearstat.append(scale_rect((351, 407, 1000, 447)))
            self.list_rect_gearstat.append(scale_rect((351, 447, 1000, 493)))
            self.list_rect_gearstat.append(scale_rect((351, 493, 1000, 535)))
            self.list_rect_gearstat.append(scale_rect((351, 535, 1000, 577)))
            self.list_rect_gearstat.append(scale_rect((351, 577, 1000, 618)))
            self.list_rect_gearstat.append(scale_rect((351, 618, 1000, 666)))


        elif math.isclose(ASPECT_RATIO_16_10, aspect, rel_tol=0.04):
            scale = width / 1600

            self.rect_check_details_page = scale_rect((467, 241, 560, 273))
            self.rect_check_gear_page = scale_rect((91, 20, 192, 67))
            self.rect_gear_name = scale_rect((257, 172, 841, 209))

            self.rect_tier = scale_rect((371, 480, 443, 515))
            self.rect_char = scale_rect((28, 393, 446, 428))
            self.rect_uni = scale_rect((25, 430, 444, 459))
            self.rect_phys_att = scale_rect((787, 289, 1008, 320))
            self.rect_energy_att = scale_rect((787, 320, 1008, 358))
            self.rect_atk_spd = scale_rect((787, 358, 1008, 395))
            self.rect_crit_rate = scale_rect((787, 395, 1008, 430))
            self.rect_crit_dam = scale_rect((787, 430, 1008, 465))
            self.rect_def_pen = scale_rect((787, 465, 1008, 502))
            self.rect_ignore_dodge = scale_rect((787, 502, 1008, 539))
            self.rect_phys_def = scale_rect((1353, 288, 1569, 321))
            self.rect_energy_def = scale_rect((1353, 321, 1569, 358))
            self.rect_hp = scale_rect((1353, 358, 1569, 395))
            self.rect_recorate = scale_rect((1353, 395, 1569, 432))
            self.rect_dodge = scale_rect((1353, 432, 1569, 468))
            self.rect_mv_spd = scale_rect((1371, 739, 1571, 776))
            self.rect_debuff = scale_rect((1459, 777, 1576, 811))
            self.rect_scd = scale_rect((1468, 811, 1574, 846))

            self.list_rect_gearstat = list()
            self.list_rect_gearstat.append(scale_rect((262, 230, 838, 265)))
            self.list_rect_gearstat.append(scale_rect((262, 265, 838, 304)))

            self.list_rect_gearstat.append(scale_rect((262, 307, 838, 340)))
            self.list_rect_gearstat.append(scale_rect((262, 340, 838, 380)))
            self.list_rect_gearstat.append(scale_rect((262, 380, 838, 419)))
            self.list_rect_gearstat.append(scale_rect((262, 419, 838, 457)))
            self.list_rect_gearstat.append(scale_rect((262, 457, 838, 494)))
            self.list_rect_gearstat.append(scale_rect((262, 494, 838, 532)))
            self.list_rect_gearstat.append(scale_rect((262, 532, 838, 571)))
            self.list_rect_gearstat.append(scale_rect((262, 571, 838, 612)))

        elif math.isclose(ASPECT_RATIO_4_3, aspect, rel_tol=0.04):
            scale = width / 1778

            self.rect_check_details_page = scale_rect((520, 378, 622, 416))
            self.rect_check_gear_page = scale_rect((96, 24, 216, 76))
            self.rect_gear_name = scale_rect((286, 300, 928, 346))

            self.rect_tier = scale_rect((412, 643, 494, 680))
            self.rect_char = scale_rect((30, 551, 497, 588))
            self.rect_uni = scale_rect((28, 586, 487, 622))
            self.rect_phys_att = scale_rect((872, 432, 1123, 467))
            self.rect_energy_att = scale_rect((872, 467, 1123, 508))
            self.rect_atk_spd = scale_rect((872, 508, 1123, 551))
            self.rect_crit_rate = scale_rect((872, 551, 1123, 588))
            self.rect_crit_dam = scale_rect((872, 588, 1123, 627))
            self.rect_def_pen = scale_rect((872, 627, 1123, 670))
            self.rect_ignore_dodge = scale_rect((872, 670, 1123, 709))
            self.rect_phys_def = scale_rect((1516, 432, 1745, 467))
            self.rect_energy_def = scale_rect((1516, 467, 1745, 508))
            self.rect_hp = scale_rect((1516, 508, 1745, 549))
            self.rect_recorate = scale_rect((1516, 549, 1745, 588))
            self.rect_dodge = scale_rect((1516, 588, 1745, 631))
            self.rect_mv_spd = scale_rect((1530, 933, 1745, 974))
            self.rect_debuff = scale_rect((1625, 976, 1747, 1011))
            self.rect_scd = scale_rect((1626, 1015, 1749, 1050))

            self.list_rect_gearstat = list()
            self.list_rect_gearstat.append(scale_rect((288, 368, 928, 407)))
            self.list_rect_gearstat.append(scale_rect((288, 407, 928, 451)))

            self.list_rect_gearstat.append(scale_rect((288, 449, 928, 492)))
            self.list_rect_gearstat.append(scale_rect((288, 492, 928, 535)))
            self.list_rect_gearstat.append(scale_rect((288, 535, 928, 577)))
            self.list_rect_gearstat.append(scale_rect((288, 577, 928, 618)))
            self.list_rect_gearstat.append(scale_rect((288, 618, 928, 659)))
            self.list_rect_gearstat.append(scale_rect((288, 659, 928, 702)))
            self.list_rect_gearstat.append(scale_rect((288, 702, 928, 744)))
            self.list_rect_gearstat.append(scale_rect((288, 744, 928, 791)))

        elif math.isclose(ASPECT_RATIO_185_9, aspect, rel_tol=0.04):
            scale = width / 1776

            self.rect_check_details_page = scale_rect((587, 200, 671, 227))
            self.rect_check_gear_page = scale_rect((79, 19, 172, 65))
            self.rect_gear_name = scale_rect((397, 133, 925, 174))

            self.rect_tier = scale_rect((499, 410, 570, 444))
            self.rect_char = scale_rect((195, 339, 564, 367))
            self.rect_uni = scale_rect((191, 367, 566, 394))
            self.rect_phys_att = scale_rect((882, 239, 1076, 271))
            self.rect_energy_att = scale_rect((882, 271, 1076, 303))
            self.rect_atk_spd = scale_rect((882, 303, 1076, 337))
            self.rect_crit_rate = scale_rect((882, 337, 1076, 369))
            self.rect_crit_dam = scale_rect((882, 369, 1076, 401))
            self.rect_def_pen = scale_rect((882, 401, 1076, 433))
            self.rect_ignore_dodge = scale_rect((882, 433, 1076, 467))
            self.rect_phys_def = scale_rect((1397, 241, 1584, 273))
            self.rect_energy_def = scale_rect((1397, 273, 1584, 303))
            self.rect_hp = scale_rect((1397, 303, 1584, 337))
            self.rect_recorate = scale_rect((1397, 337, 1584, 369))
            self.rect_dodge = scale_rect((1397, 369, 1584, 401))
            self.rect_mv_spd = scale_rect((1406, 644, 1587, 681))
            self.rect_debuff = scale_rect((1491, 680, 1585, 713))
            self.rect_scd = scale_rect((1486, 712, 1584, 742))

            self.list_rect_gearstat = list()
            self.list_rect_gearstat.append(scale_rect((406, 190, 919, 220)))
            self.list_rect_gearstat.append(scale_rect((406, 220, 919, 257)))

            self.list_rect_gearstat.append(scale_rect((406, 257, 919, 289)))
            self.list_rect_gearstat.append(scale_rect((406, 289, 919, 325)))
            self.list_rect_gearstat.append(scale_rect((406, 325, 919, 358)))
            self.list_rect_gearstat.append(scale_rect((406, 358, 919, 392)))
            self.list_rect_gearstat.append(scale_rect((406, 392, 919, 426)))
            self.list_rect_gearstat.append(scale_rect((406, 426, 919, 461)))
            self.list_rect_gearstat.append(scale_rect((406, 461, 919, 495)))
            self.list_rect_gearstat.append(scale_rect((406, 495, 919, 531)))

        elif math.isclose(ASPECT_RATIO_3_2, aspect, rel_tol=0.04):
            scale = width / 1500

            self.rect_check_details_page = scale_rect((438, 255, 528, 288))
            self.rect_check_gear_page = scale_rect((81, 19, 186, 63))
            self.rect_gear_name = scale_rect((243, 190, 778, 231))

            self.rect_tier = scale_rect((349, 478, 415, 513))
            self.rect_char = scale_rect((25, 403, 415, 433))
            self.rect_uni = scale_rect((25, 433, 415, 460))
            self.rect_phys_att = scale_rect((738, 298, 946, 331))
            self.rect_energy_att = scale_rect((738, 331, 946, 369))
            self.rect_atk_spd = scale_rect((738, 369, 946, 400))
            self.rect_crit_rate = scale_rect((738, 400, 946, 435))
            self.rect_crit_dam = scale_rect((738, 435, 946, 469))
            self.rect_def_pen = scale_rect((738, 469, 946, 501))
            self.rect_ignore_dodge = scale_rect((738, 501, 946, 537))
            self.rect_phys_def = scale_rect((1279, 301, 1476, 333))
            self.rect_energy_def = scale_rect((1279, 333, 1476, 367))
            self.rect_hp = scale_rect((1279, 367, 1476, 400))
            self.rect_recorate = scale_rect((1279, 400, 1476, 435))
            self.rect_dodge = scale_rect((1279, 435, 1476, 469))
            self.rect_mv_spd = scale_rect((1291, 721, 1474, 759))
            self.rect_debuff = scale_rect((1372, 759, 1476, 792))
            self.rect_scd = scale_rect((1380, 790, 1476, 829))

            self.list_rect_gearstat = list()
            self.list_rect_gearstat.append(scale_rect((246, 246, 786, 279)))
            self.list_rect_gearstat.append(scale_rect((246, 279, 786, 318)))

            self.list_rect_gearstat.append(scale_rect((246, 316, 786, 352)))
            self.list_rect_gearstat.append(scale_rect((246, 352, 786, 390)))
            self.list_rect_gearstat.append(scale_rect((246, 390, 786, 423)))
            self.list_rect_gearstat.append(scale_rect((246, 423, 786, 459)))
            self.list_rect_gearstat.append(scale_rect((246, 459, 786, 496)))
            self.list_rect_gearstat.append(scale_rect((246, 496, 786, 531)))
            self.list_rect_gearstat.append(scale_rect((246, 531, 786, 565)))
            self.list_rect_gearstat.append(scale_rect((246, 565, 786, 603)))

        else:
            raise UnsupportedRatioException
        print("Scale = " + str(scale))

list_gear_dict = (("physical_attack_by_level", "physicalattackperlv.", 1),
                  ("physical_attack", "physicalattack", 1),
                  ("energy_attack_by_level", "energyattackperlv.", 1),
                  ("energy_attack", "energyattack", 1),
                  ("hp_by_level", "hpperlv.", 3),
                  ("hp", "hp", 3),
                  ("defense_penetration", "ignoredefense", 4),
                  ("critical_rate", "criticalrate", 4),
                  ("critical_damage", "criticaldamage", 4),
                  ("skill_cooldown", "skillcooldown", 4),
                  ("attack_speed", "attackspeed", 4),
                  ("all_attack", "allattacks", 1),
                  ("dodge", "dodge", 3),
                  ("movement_speed", "movementspeed", 3),
                  ("recovery_rate", "recoveryrate", 3),
                  ("physical_defense_by_level", "physicaldefenseperlv.", 2),
                  ("energy_defense_by_level", "energydefenseperlv.", 2),
                  ("physical_defense", "physicaldefense", 2),
                  ("energy_defense", "energydefense", 2),
                  ("all_defense", "alldefenses", 2))
list_gear_val = ()
list_gear_statname = ()


class GearValue:
    def __init__(self):
        self.type = ""
        self.val = 0.
        # self.pref = False


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
    return ocr_ob.ocr_using_color_similarity(image.crop(rect), color=color, threshold=threshold,
                                             inverted_colors=inverted_colors)


def color_ocr_int(image, rect, color=(255, 255, 255), threshold=120, inverted_colors=False):
    num = ocr_ob.ocr_using_color_similarity(image.crop(rect), color=color, threshold=threshold,
                                            inverted_colors=inverted_colors)
    try:
        num = int(
            num.replace(" ", "").replace("%", "").replace("+", "").replace('"', "4").replace("s", "5").replace("o",
                                                                                                               "0").replace(
                "d", "0").replace("z", "2").replace(".", "").replace(",", "").replace("'", ""))
    except:
        num = 0
    return num


def color_ocr_float(image, rect, color=(255, 255, 255), threshold=120, inverted_colors=False):
    num = ocr_ob.ocr_using_color_similarity(image.crop(rect), color=color, threshold=threshold,
                                            inverted_colors=inverted_colors)
    try:
        num = float(
            num.replace(" ", "").replace("%", "").replace("+", "").replace('"', "4").replace("s", "5").replace("o",
                                                                                                               "0").replace(
                "d", "0").replace("z", "2").replace(",", ".").replace("-", ".").replace("'", ""))
    except:
        num = 0.
    return num


def get_gear(screenshot, rects, gearis5):
    # split gear state rectangle into left and right
    def split_gear_rect(rect):
        return ((rect[0], rect[1], int((rect[2] - rect[0]) * 0.7 + rect[0]), rect[3]),
                (rect[2] - int((rect[2] - rect[0]) * 0.3), rect[1], rect[2], rect[3]))

    def do_ocr(image, rect):
        stat_rects = split_gear_rect(rect)

        # split rects to cover gear attribute & values separately
        left_rect = stat_rects[0]
        right_rect = stat_rects[1]

        # get raw ocr result
        raw_type = color_ocr_text(image, left_rect, color=(10, 18, 35), threshold=100, inverted_colors=True).replace(
            " ", "").lower()
        gear_type = ""
        gear_num = -1

        if raw_type != "":
            # this step checks for 'exact' match
            for item in list_gear_dict:
                if item[1] in raw_type:
                    perinitem = "per" in item[1]
                    perinraw = "per" in raw_type

                    # "per" has to be in both or not in both for an exact match
                    if (perinitem and perinraw) or (not perinitem and not perinraw):
                        gear_type = item[0]
                        gear_num = item[2]
                        break
            # otherwise find nearest attribute match
            if gear_type == "":
                threshold = 3
                for item in list_gear_dict:
                    distance = Levenshtein.distance(item[1], raw_type)
                    if distance < threshold:
                        gear_type = item[0]
                        gear_num = item[2]
                        threshold = distance

        val = color_ocr_float(image, right_rect, color=(10, 18, 35), inverted_colors=True)
        if val != "":
            try:
                val = float(val)
            except:
                val = 0.
        else:
            val = 0.
        return gear_type, val, gear_num

    gear = [GearValue() for i in range(8)]
    gearnum = do_ocr(screenshot, rects[0])[2]
    offset = 1 if gearis5 else 2
    for i in range(8):
        gear[i].type, gear[i].val, num = do_ocr(screenshot, rects[i+offset])

    return gear, gearnum


def get_char_json(filepath):
    screenshot = Image.open(filepath)

    # now = datetime.datetime.now()
    desiredwidth = 1920
    scale = desiredwidth / screenshot.size[0]
    if screenshot.size[0] < desiredwidth:
        screenshot = screenshot.resize((desiredwidth, int(scale * screenshot.size[1])), Image.NEAREST)
    elif screenshot.size[0] > desiredwidth:
        screenshot.thumbnail((int(screenshot.size[0] * scale), int(screenshot.size[1] * scale)))
    # print("scaled in "+str(datetime.datetime.now()-now))

    time = datetime.datetime.now()
    width = screenshot.size[0]
    height = screenshot.size[1]

    # define rects based on aspect ratio
    try:
        rects = Rects(width, height)
    except UnsupportedRatioException:
        e = UnsupportedRatioException()
        e.message = filepath
        return e

    if color_ocr_text(screenshot, rects.rect_check_details_page, color=(23, 23, 57), threshold=90,
                      inverted_colors=True).replace(" ", "") == "attack":

        char = Character()

        char.tier = 2 if (
            "2" in color_ocr_text(screenshot, rects.rect_tier, (18, 25, 47), threshold=90,
                                  inverted_colors=True).replace(
                "z", "2")) else 1
        char.id = get_char_alias(color_ocr_text(screenshot, rects.rect_char, color=(10, 18, 35), inverted_colors=True))
        char.uniform = get_uniform_alias(
            color_ocr_text(screenshot, rects.rect_uni, color=(10, 18, 35), inverted_colors=True))

        char.attack.physical = color_ocr_int(screenshot, rects.rect_phys_att, color=(255, 255, 255), threshold=100)
        char.attack.energy = color_ocr_int(screenshot, rects.rect_energy_att, color=(255, 255, 255), threshold=100)
        char.atkspeed = color_ocr_float(screenshot, rects.rect_atk_spd, color=(255, 255, 255), threshold=100)
        char.critrate = color_ocr_float(screenshot, rects.rect_crit_rate, color=(255, 255, 255), threshold=100)
        char.critdamage = color_ocr_float(screenshot, rects.rect_crit_dam, color=(255, 255, 255), threshold=100)
        char.defpen = color_ocr_float(screenshot, rects.rect_def_pen, color=(255, 255, 255), threshold=100)
        char.ignore_dodge = color_ocr_float(screenshot, rects.rect_ignore_dodge, color=(255, 255, 255), threshold=100)
        char.defense.physical = color_ocr_int(screenshot, rects.rect_phys_def, color=(255, 255, 255), threshold=100)
        char.defense.energy = color_ocr_int(screenshot, rects.rect_energy_def, color=(255, 255, 255), threshold=100)
        char.hp = color_ocr_int(screenshot, rects.rect_hp, color=(255, 255, 255), threshold=100)
        char.recorate = color_ocr_float(screenshot, rects.rect_recorate, color=(255, 255, 255), threshold=100)
        char.dodge = color_ocr_float(screenshot, rects.rect_dodge, color=(255, 255, 255), threshold=100)
        char.movspeed = color_ocr_float(screenshot, rects.rect_mv_spd, color=(255, 255, 255), threshold=100)
        char.debuff = color_ocr_float(screenshot, rects.rect_debuff, color=(255, 255, 255), threshold=100)
        char.scd = color_ocr_float(screenshot, rects.rect_scd, color=(255, 255, 255), threshold=100)

        return {"type": "details", "result_char": char, "filepath": filepath}

    elif color_ocr_text(screenshot, rects.rect_check_gear_page, color=(10, 18, 35), inverted_colors=True,
                        threshold=140).replace(" ", "") == "gear":

        gear_name_and_level = color_ocr_text(screenshot, rects.rect_gear_name, inverted_colors=True,color=(28,44,60), threshold=125).split("+")
        gear_name = gear_name_and_level[0].strip()
        gear_level_string = gear_name_and_level[1].strip().lower().replace("s", "5").replace("l", "1")
        gear_is_5 = "5" in gear_level_string and "1" not in gear_level_string

        # returns list of dicts from DB with format (char_alias, gear_name, gear_num)
        char_list = get_chars_from_gear(gear_name)

        # if managed to match to exactly 1 character, return character json, else :
        char = Character()

        if len(char_list) == 0:
            return filepath
        elif len(char_list) == 1:
            char.id = char_list[0]["id"]
            # database returns gear numbers 1-4
            gear_num = char_list[0]["gear_num"]
            char.gear[gear_num - 1] = get_gear(screenshot, rects.list_rect_gearstat, gear_is_5)[0]
            char.uniform = get_default_uni(char.id)

            return {"type": "gear", "result_char": char, "char_list": char_list, "gear_num": gear_num,
                    "gear_name": gear_name, "filepath": filepath}
        else:
            # return (char_list, gear_stats_list) where gear_stats_list is a list of 8 GearValue objects
            gear_result, gear_num = get_gear(screenshot, rects.list_rect_gearstat, gear_is_5)
            if gear_num == -1:
                return {"type": "gear_dup", "char_list": char_list, "gear": gear_result, "filepath": filepath}
            else:
                char_list_filtered = list()
                for item in char_list:
                    if item["gear_num"] == gear_num:
                        char_list_filtered.append(item)
                if char_list_filtered == 0:
                    return filepath
                else:
                    return {"type": "gear_dup", "char_list": char_list_filtered, "gear": gear_result, "filepath": filepath}

    else:
        return filepath


if __name__ == '__main__':
    time = datetime.datetime.now()

    # print(get_char_json('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-31.png'))
    print(get_char_json('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-28-12-13-38.png'))
    # print(get_char_json('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-04-02-02-02-33.png'))
    print(get_char_json('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-31 - Copy.jpg'))
    print(datetime.datetime.now() - time)
