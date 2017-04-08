import datetime

import Levenshtein
import jsonpickle
from PIL import Image
from mff.databasehelper import *

from mff.ocr import Ocr


class UnsupportedRatioException(ValueError):
    pass


ocr_ob = Ocr()


class Rects:
    def __init__(self, width: int, height: int):

        aspect = width / height
        scale = 1.

        def scale_rect(rect):
            return tuple(int(scale * i) for i in rect)

        if aspect == 16 / 9:
            scale = width / 1920

            self.rect_check_details_page = scale_rect((586, 184, 733, 223))
            self.rect_check_gear_page = scale_rect((156, 23, 313, 74))
            self.rect_gear_name = scale_rect((387, 143, 1018, 187))

            self.rect_tier = scale_rect((460, 393, 555, 427))
            self.rect_char = scale_rect((104, 479, 546, 520))
            self.rect_uni = scale_rect((108, 523, 554, 560))
            self.rect_phys_att = scale_rect((911, 240, 1186, 280))
            self.rect_energy_att = scale_rect((911, 280, 1186, 327))
            self.rect_atk_spd = scale_rect((911, 327, 1186, 374))
            self.rect_crit_rate = scale_rect((911, 374, 1186, 423))
            self.rect_crit_dam = scale_rect((911, 423, 1186, 468))
            self.rect_def_pen = scale_rect((911, 468, 1186, 517))
            self.rect_ignore_dodge = scale_rect((911, 517, 1186, 568))
            self.rect_phys_def = scale_rect((1530, 238, 1816, 280))
            self.rect_energy_def = scale_rect((1530, 280, 1816, 329))
            self.rect_hp = scale_rect((1530, 329, 1816, 376))
            self.rect_recorate = scale_rect((1530, 376, 1816, 421))
            self.rect_dodge = scale_rect((1530, 421, 1816, 472))
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

        elif aspect == 16 / 10:
            self.rect_check_details_page = scale_rect((586, 184, 733, 223))
            self.rect_check_gear_page = scale_rect((156, 23, 313, 74))
            self.rect_gear_name = scale_rect((387, 143, 1018, 187))

            self.rect_tier = scale_rect((460, 393, 555, 427))
            self.rect_char = scale_rect((104, 479, 546, 520))
            self.rect_uni = scale_rect((108, 523, 554, 560))
            self.rect_phys_att = scale_rect((911, 240, 1186, 280))
            self.rect_energy_att = scale_rect((911, 280, 1186, 327))
            self.rect_atk_spd = scale_rect((911, 327, 1186, 374))
            self.rect_crit_rate = scale_rect((911, 374, 1186, 423))
            self.rect_crit_dam = scale_rect((911, 423, 1186, 468))
            self.rect_def_pen = scale_rect((911, 468, 1186, 517))
            self.rect_ignore_dodge = scale_rect((911, 517, 1186, 568))
            self.rect_phys_def = scale_rect((1530, 238, 1816, 280))
            self.rect_energy_def = scale_rect((1530, 280, 1816, 329))
            self.rect_hp = scale_rect((1530, 329, 1816, 376))
            self.rect_recorate = scale_rect((1530, 376, 1816, 421))
            self.rect_dodge = scale_rect((1530, 421, 1816, 472))
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

        elif aspect == 4 / 3:
            return

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
        self.percent = 0.


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

        self.ocr_type = ""
        self.ocr_gear_num = -1

    # remove last 2 attributes from state so jsonpickler does not serialise them
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['ocr_type']
        del state['ocr_gear_num']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


def greyscale_ocr(image, rect, threshold=140):
    return ocr_ob.ocr_using_greyscale(image.crop(rect), threshold)

def color_ocr(image, rect, color, threshold=50):
    return ocr_ob.ocr_using_color_similarity(image.crop(rect), color=color, similarity=threshold)


def get_gear(screenshot, rects):
    # split gear state rectangle into left and right
    def split_gear_rect(rect):
        return ((rect[0], rect[1], int((rect[2] - rect[0]) * 0.8 + rect[0]), rect[3]),
                (rect[2] - int((rect[2] - rect[0]) * 0.2), rect[1], rect[2], rect[3]))

    def do_ocr(image, rect):
        stat_rects = split_gear_rect(rect)
        left_rect = stat_rects[0]
        right_rect = stat_rects[1]

        type = ""
        raw_type = greyscale_ocr(image, left_rect, threshold=70).replace(" ", "").lower()
        if raw_type != "":
            for i, item in enumerate(list_gear_statname):
                if item in raw_type:
                    type = list_gear_val[i]
            if type == "":
                for i, item in enumerate(list_gear_statname):
                    if Levenshtein.distance(item, raw_type) < 3:
                        type = list_gear_val[i]
        val = color_ocr(image, right_rect, color="#0A1223", threshold=50).replace(" ", "").replace("%", "").replace("+", "").replace('"', "4")
        # val = greyscale_ocr(image, right_rect, threshold=145).replace(" ", "").replace("%", "").replace("+", "").replace('"', "4")
        if val != "":
            print(val)
            val = float(val)
        else:
            val = 0.

        return type, val

    gear = [GearValue() for i in range(8)]
    for i, item in enumerate(rects):
        gear[i].type, gear[i].val = do_ocr(screenshot, rects[i])
    return gear


def get_char_json(filepath):

    screenshot = Image.open(filepath)


    time = datetime.datetime.now()
    width = screenshot.size[0]
    height = screenshot.size[1]
    # define rects based on aspect ratio

    try:
        rects = Rects(width, height)
    except UnsupportedRatioException:
        return UnsupportedRatioException

    if greyscale_ocr(screenshot, rects.rect_check_details_page, threshold=100) == "attack":

        char = Character()

        char.tier = 2 if ("2" in greyscale_ocr(screenshot, rects.rect_tier, 180)) else 1
        char.id = get_char_alias(greyscale_ocr(screenshot, rects.rect_char, 180))
        char.uniform = get_uniform_alias(greyscale_ocr(screenshot, rects.rect_uni, 180))
        char.attack.physical = greyscale_ocr(screenshot, rects.rect_phys_att, 240)
        char.attack.energy = greyscale_ocr(screenshot, rects.rect_energy_att, 240)
        char.atkspeed = greyscale_ocr(screenshot, rects.rect_atk_spd, 240)
        char.critrate = greyscale_ocr(screenshot, rects.rect_crit_rate, 240)
        char.critdamage = greyscale_ocr(screenshot, rects.rect_crit_dam, 240)
        char.defpen = greyscale_ocr(screenshot, rects.rect_def_pen, 240)
        char.ignore_dodge = greyscale_ocr(screenshot, rects.rect_ignore_dodge, 240)
        char.defense.physical = greyscale_ocr(screenshot, rects.rect_phys_def, 240)
        char.defense.energy = greyscale_ocr(screenshot, rects.rect_energy_def, 240)
        char.hp = greyscale_ocr(screenshot, rects.rect_hp, 240)
        char.recorate = greyscale_ocr(screenshot, rects.rect_recorate, 240)
        char.dodge = greyscale_ocr(screenshot, rects.rect_dodge, 240)
        char.movspeed = greyscale_ocr(screenshot, rects.rect_mv_spd, 240)
        char.debuff = greyscale_ocr(screenshot, rects.rect_debuff, 240)
        char.scd = greyscale_ocr(screenshot, rects.rect_scd, 240)

        return {"result_json": '"' + char.id + '":' + jsonpickle.encode(char, unpicklable=False), "filepath": filepath}

    elif greyscale_ocr(screenshot, rects.rect_check_gear_page, threshold=100) == "gear":

        gear_name = greyscale_ocr(screenshot, rects.rect_gear_name, threshold=230)

        # returns list of dicts from DB with format (char_alias, gear_name, gear_num)
        char_list = get_chars_from_gear(gear_name)

        # if managed to match to exactly 1 character, return character json, else :
        char = Character()
        if len(char_list) == 1:
            char.id = char_list[0]["char_alias"]
            # database returns gear numbers 1-4, have to zero it
            gear_num = char_list[0]["gear_num"] - 1
            char.gear[gear_num] = get_gear(screenshot, rects.list_rect_gearstat)
            char.uniform = get_default_uni(char.id)

            print(char.id)

            return {"result_json": '"' + char.id + '":' + jsonpickle.encode(char, unpicklable=False), "filepath": filepath}
        else:
            # return (char_list, gear_stats_list) where gear_stats_list is a list of 8 GearValue objects
            gear_result = get_gear(screenshot, rects.list_rect_gearstat)
            return {"char_list": char_list, "gear_json": jsonpickle.encode(gear_result, unpicklable=False),
                    "filepath": filepath}
    else:
        return filepath


if __name__ == '__main__':
    time = datetime.datetime.now()

    # print(get_char_json('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-31.png'))
    print(get_char_json('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-28-12-13-38.png'))
    # print(get_char_json('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-04-02-02-02-33.png'))
    print(get_char_json('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-31 - Copy.jpg'))
    print(datetime.datetime.now() - time)
