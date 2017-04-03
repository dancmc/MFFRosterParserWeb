import datetime
import multiprocessing
from mffhelper import get_char_json



screenshot_list = list()
screenshot = 'C:/Users/Daniel/Nox_share/Image/Screenshot_2017-04-02-02-02-33.png'
screenshot1 = 'C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-31 - Copy.jpg'
screenshot_list.append(screenshot)
screenshot_list.append(screenshot1)
screenshot_list.append(screenshot1)
screenshot_list.append(screenshot1)
screenshot_list.append(screenshot1)
screenshot_list.append(screenshot1)
screenshot_list.append(screenshot1)
screenshot_list.append(screenshot1)
screenshot_list.append(screenshot1)
screenshot_list.append(screenshot1)
screenshot_list.append(screenshot1)
screenshot_list.append(screenshot1)
screenshot_list.append(screenshot1)
screenshot_list.append(screenshot1)
screenshot_list.append(screenshot1)


def get_time(func):
    def func_wrapper(*args, **kwargs):
        time1 = datetime.datetime.now()
        result = func(*args, **kwargs)
        print(datetime.datetime.now() - time1)
        return result
    return func_wrapper

# if there are duplicate gears between characters, display pic and ask user to select char manually
def ask_user(char_list):

    pass

# if there were no matches found for image, display image and say failed
def image_proc_failed():
    pass

result_list = []

def log_result(result):
    if result is None:
        image_proc_failed()
    elif type(result) is list:
        ask_user(result)
    elif type(result)is str:
        result_list.append(result)

if __name__ == '__main__':

    time = datetime.datetime.now()

    pool = multiprocessing.Pool(processes=None)
    for i in screenshot_list:
        pool.apply_async(get_char_json, args=(i,), callback=log_result)
    pool.close()
    pool.join()

    print(datetime.datetime.now() - time)
    print("\n".join(result_list))
