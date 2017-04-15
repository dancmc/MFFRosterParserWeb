import datetime
import tesserocr

from PIL import Image

from mffstuff.ocr_scripts import ocr

screenshots = list()
screenshots.append(Image.open('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-31 - Copy.jpg'))

time = datetime.datetime.now()

# for screenshot in screenshots:
#     screenshot = ocr.binarise_greyscale_image(screenshot.crop((400, 304, 1024, 349)), 200)
#     print(tesserocr.image_to_text(screenshot))


ocrob = ocr.Ocr()
list_detail_rects = {
    "rect_tier": (460, 393, 555, 427),
    "rect_char": (104, 479, 546, 520),
    "rect_uni": (108, 523, 554, 560),
    "rect_phys_att": (911, 240, 1186, 280),
    "rect_energy_att": (911, 280, 1186, 327),
    "rect_atk_spd": (911, 327, 1186, 374),
    "rect_crit_rate": (911, 374, 1186, 423),
    "rect_crit_dam": (911, 423, 1186, 468),
    "rect_def_pen": (911, 468, 1186, 517),
    "rect_ignore_dodge": (911, 517, 1186, 568),
    "rect_phys_def": (1530, 238, 1816, 280),
    "rect_energy_def": (1530, 280, 1816, 329),
    "rect_hp": (1530, 329, 1816, 376),
    "rect_recorate": (1530, 376, 1816, 421),
    "rect_dodge": (1530, 421, 1816, 472),
    "rect_mv_spd": (1541, 810, 1814, 847),
    "rect_debuff": (1653, 856, 1816, 895),
    "rect_scd": (1666, 903, 1816, 937)}

list_detail_rects_tess = [{'y': 329, 'x': 1530, 'w': 286, 'h': 47}, {'y': 856, 'x': 1653, 'w': 163, 'h': 39},
                          {'y': 479, 'x': 104, 'w': 442, 'h': 41}, {'y': 423, 'x': 911, 'w': 275, 'h': 45},
                          {'y': 393, 'x': 460, 'w': 95, 'h': 34}, {'y': 903, 'x': 1666, 'w': 150, 'h': 34},
                          {'y': 523, 'x': 108, 'w': 446, 'h': 37}, {'y': 376, 'x': 1530, 'w': 286, 'h': 45},
                          {'y': 280, 'x': 1530, 'w': 286, 'h': 49}, {'y': 421, 'x': 1530, 'w': 286, 'h': 51},
                          {'y': 517, 'x': 911, 'w': 275, 'h': 51}, {'y': 327, 'x': 911, 'w': 275, 'h': 47},
                          {'y': 280, 'x': 911, 'w': 275, 'h': 47}, {'y': 374, 'x': 911, 'w': 275, 'h': 49},
                          {'y': 238, 'x': 1530, 'w': 286, 'h': 42}, {'y': 468, 'x': 911, 'w': 275, 'h': 49},
                          {'y': 240, 'x': 911, 'w': 275, 'h': 40}, {'y': 810, 'x': 1541, 'w': 273, 'h': 37}]

# result = list()
# for k, v in list_detail_rects.items():
#     result.append({"x": v[0], "y": v[1], "w": v[2] - v[0], "h": v[3] - v[1]})
#
# print(result)

tesserocr.file_to_text()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Using multiple instances of tesserocr, no threads, least efficient - 2.6s
#
# screenshot = Image.open('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-31 - Copy.jpg')
# for k, v in list_detail_rects.items():
#     intermediate = ocr.binarise_greyscale_image(screenshot.crop(v), 200)
#     print(tesserocr.image_to_text(intermediate))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Using single instance of tesserocr object, no threads (current impl) - 0.57s, 0.266(4 rects)
#
# screenshot = Image.open('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-31 - Copy.jpg')
# for k, v in list_detail_rects.items():
#     print(ocrob.ocr_using_greyscale(screenshot.crop(v), 200))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Using multiple instances of tesserocr, with threading - 0.88s, 0.312 (4 rects)
#
# # lock to serialize console output
# lock = threading.Lock()
#
# screenshot = Image.open('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-31 - Copy.jpg')
# def do_work(item):
#     item = ocr.binarise_greyscale_image(item, 200)
#     output = tesserocr.image_to_text(item)
#     # Make sure the whole print completes or threads can mix up output in one line.
#     with lock:
#         print(threading.current_thread().name, output)
#
#
# # The worker thread pulls an item from the queue and processes it
# def worker():
#     while True:
#         screenshot = q.get()
#         do_work(screenshot)
#         q.task_done()
#
#
# # Create the queue and thread pool.
# q = Queue()
# for i in range(8):
#     t = threading.Thread(target=worker)
#     t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
#     t.start()
#
# # stuff work items on the queue (in this case, just a number).
# for k,v in list_detail_rects.items():
#     q.put(screenshot.crop(v))
#
# q.join()  # block until all tasks are done


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Using multiple instances of tesserocr, with threading & boxes - 1.35s
# lock to serialize console output
# lock = threading.Lock()
#
# screenshot = Image.open('C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-31 - Copy.jpg')
# screenshot = ocr.binarise_greyscale_image(screenshot, 200)
#
# print(datetime.datetime.now() - time)
#
# def do_work(box):
#
#     with tesserocr.PyTessBaseAPI() as api:
#         api.SetImage(screenshot)
#         api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
#         output = api.GetUTF8Text()
#     # Make sure the whole print completes or threads can mix up output in one line.
#     with lock:
#         print(threading.current_thread().name, output)
#
#
# # The worker thread pulls an item from the queue and processes it
# def worker():
#     while True:
#         screenshot = q.get()
#         do_work(screenshot)
#         q.task_done()
#
#
# # Create the queue and thread pool.
# q = Queue()
# for i in range(8):
#     t = threading.Thread(target=worker)
#     t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
#     t.start()
#
# # stuff work items on the queue (in this case, just a number).
#
# for v in list_detail_rects_tess:
#     q.put(v)
#
# q.join()  # block until all tasks are done


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Using single instance of tesserocr, with threading - non-starter


print(datetime.datetime.now() - time)
