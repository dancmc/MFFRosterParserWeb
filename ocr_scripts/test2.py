char='C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-31 - Copy.jpg'
txt = 'C:/Users/Daniel/Nox_share/Image/training/eng.mff.exp0.box'
# gears = 'C:/Users/Daniel/Nox_share/Image/Screenshot_2017-03-23-22-51-17.png'
# wFile = '/var/www/app_dancmc/ocr/uploaded_screenshots/test.jpg'
# wFile2 = '/var/www/app_dancmc/ocr/uploaded_screenshots/testPIL.jpg'
#
# # with WImage(filename=char, resolution=900) as image:
# #     image.compression_quality = 99
# #     image.save(filename=wFile)
# #
# # (Image.open(char)).save(wFile2, "JPEG")
#
#
# now = datetime.datetime.now()
#
# screenshot = Image.open(char)
# screenshot = screenshot.crop((911, 374, 1186, 423))
# # screenshot.show()
#
# ocr.binarise_color_image(screenshot, (255,255,255), 40, erode=True)
#
# print(datetime.datetime.now()-now)
# opencv = ocr.PIL_to_opencv(screenshot)
# kernel = numpy.zeros((1,1),numpy.uint8)
# opencv = cv2.erode(opencv, kernel, iterations=1)
# ocr.opencv_to_PIL(opencv).show()

# ocr.binarise_color_image(Image.open(char), threshold=170, erode=True).show()
# import collections
# with open(txt) as f:
#     char_list = list(f)
#
#     char_list = [c[0] for c in char_list]
#
#
#     char_list.sort()
#     chardict = dict(collections.Counter(char_list))
#
#     # d = chardict.items()
#     chardict = collections.OrderedDict(sorted(chardict.items(), key=lambda n: n[1], reverse=True))
#     f.close()
# # list_txt = list((f.read()).replace(" ","").replace("\n",""))
# list_alpha = list("qwertyuiopasdfghjklzmxncbvQWERTYUIOPLAKSJDHFGZXCVBNM")
# print([x for x in list_alpha if x not in char_list])
# for k, v in chardict.items():
#     print(k +" : "+ str(v))

val = ['(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)']*0
print(val)