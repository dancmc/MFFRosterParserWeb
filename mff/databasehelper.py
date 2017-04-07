from flask import g
import Levenshtein


def connect():
    try:
        cur = g.db_conn.cursor()
        return cur
    except:
        print("unable to connect")


def get_chars_from_gear(ocr_output):
    cur = connect()
    result_list = list()


    # try to find exact match for gear name
    sql = "SELECT char_alias, gear1 as gear_name, '1' AS gear_num FROM mff WHERE %s = gear1 GROUP BY char_alias, gear1 " \
          "UNION SELECT char_alias, gear2, '2' AS gear_num FROM mff WHERE %s = gear2 GROUP BY char_alias, gear2 " \
          "UNION SELECT char_alias, gear3, '3' AS gear_num FROM mff WHERE %s = gear3 GROUP BY char_alias, gear3 " \
          "UNION SELECT char_alias, gear4, '4' AS gear_num FROM mff WHERE %s = gear4 GROUP BY char_alias, gear4"
    data = (ocr_output, ocr_output, ocr_output, ocr_output,)
    cur.execute(sql, data)

    rows = cur.fetchall()
    for row in rows:
        result_list.append({"char_alias" : row[0], "gear_name" : row[1], "gear_num" : int(row[2])})

    # if no exact match, try to find close match
    if cur.rowcount == 0:
        sql = "SELECT char_alias, gear1 as gear_name, '1' AS gear_num FROM mff " \
              "UNION SELECT char_alias, gear2, '2' AS gear_num FROM mff " \
              "UNION SELECT char_alias, gear3, '3' AS gear_num FROM mff " \
              "UNION SELECT char_alias, gear4, '4' AS gear_num FROM mff"
        cur.execute(sql)

        rows = cur.fetchall()
        for row in rows:
            # for short words, more leeway (arbitrary thresholds)
            threshold = 4 if len(ocr_output) > 8 else 3

            if Levenshtein.distance(ocr_output, row[1]) < threshold:
                result_list.append({"char_alias" : row[0], "gear_name" : row[1], "gear_num" : int(row[2])})

    # there may be more than 1 character with the same gear (in potentially different slots)
    # return list of tuples in format (char_alias, gear name, gear number)
    cur.close()
    return result_list


def get_char_alias(char_name):
    cur = connect()

    data = (char_name,)
    SQL = "SELECT char_alias FROM mff WHERE %s = char"
    cur.execute(SQL, data)

    char_alias = ""
    if cur.rowcount>0:
        rows = cur.fetchall()
        char_alias = rows[0][0]
    else:
        SQL = "SELECT char_alias, char FROM mff"
        cur.execute(SQL)
        rows = cur.fetchall()
        for row in rows:
            threshold = 4 if len(char_name) > 8 else 3
            if Levenshtein.distance(char_name, row[1]) < threshold:
                char_alias = row[0]

    cur.close()
    return char_alias

def get_uniform_alias(uni_name):
    cur = connect()

    data = (uni_name,)
    SQL = "SELECT uni_alias FROM mff WHERE %s = uni"
    cur.execute(SQL, data)

    uni_alias = ""
    if cur.rowcount > 0:
        rows = cur.fetchall()
        uni_alias = rows[0][0]
    else:
        SQL = "SELECT uni_alias, uni FROM mff"
        cur.execute(SQL)
        rows = cur.fetchall()
        for row in rows:
            threshold = 5 if len(uni_name) > 10 else 3
            if Levenshtein.distance(uni_name, row[1]) < threshold:
                uni_alias = row[0]

    cur.close()
    return uni_alias

def get_default_uni(char_alias):
    cur = connect()

    data = (char_alias,)
    SQL = "SELECT uni_alias FROM mff WHERE %s = char_alias LIMIT 1"
    cur.execute(SQL, data)
    rows = cur.fetchall()
    default_uni = rows[0][0]

    cur.close()
    return default_uni