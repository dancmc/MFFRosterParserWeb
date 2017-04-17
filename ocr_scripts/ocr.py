from PIL import Image, ImageColor, ImageFilter
import numpy
import math
import tesserocr
import cv2
from datetime import datetime

def is_color_similar(color1, color2, similarity):
    threshold = math.pow(similarity, 2) * 3

    color2 = ImageColor.getrgb(color2)
    # lambda acts as a for loop iterating over elements of arguments
    color_diff = sum(tuple(map(lambda x, y: math.pow(x - y, 2), color1, color2)))
    return color_diff <= threshold

def opencv_to_PIL(opencv):
    PILarray = opencv[:, :, ::-1]
    return Image.fromarray(PILarray.astype('uint8'))

def PIL_to_opencv(image):
    rgbimg = Image.new("RGB", image.size)
    rgbimg.paste(image)
    PILarray = numpy.array(rgbimg, numpy.uint8)
    return PILarray[:, :, ::-1]

def reverse_numpy(array):
    return array[:, :, ::-1]

def reverse_grey_numpy(array):
    return array[:, ::-1]


def binarise_greyscale_image(im, threshold=150):
    # in RBG, 3d array contains (row) number of arrays of (column) elements each. Each element is an RBG array
    monochrome_image = im.convert('L')

    bw_array = numpy.where(numpy.array(monochrome_image, numpy.uint8) > threshold, 255, 0)

    bw_image = Image.fromarray(bw_array.astype('uint8'))
    rgbimg = Image.new("RGB", bw_image.size)
    rgbimg.paste(bw_image)

    return rgbimg

def binarise_color_image(im, wanted_rgbtuple=(255,255,255), threshold=120, inverted_colors=False):

    output_img = PIL_to_opencv(im)

    output_img = cv2.resize(output_img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    output_img = cv2.blur(output_img, (5, 5))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    output_img = cv2.erode(output_img, kernel, iterations=1)


    lower_color = numpy.array([max(0, x-threshold) for x in wanted_rgbtuple])[::-1]
    upper_color = numpy.array([min(255, x + threshold) for x in wanted_rgbtuple])[::-1]
    mask = cv2.inRange(output_img, lower_color, upper_color)

    # mask a blank image instead of original - get a binarised image instead of original color
    output_img = output_img.copy()
    output_img = output_img.astype(numpy.uint8)
    output_img[:] = 255
    output_img = cv2.bitwise_and(output_img, output_img, mask=mask)

    # usually wanted_rgbtuple should be text color. if background color retained, invert flag should be set
    if(inverted_colors):
        output_img = numpy.where(output_img[:,:,:]==0, 255, 0, )
        output_img = output_img.astype(numpy.uint8)

    output_img = cv2.copyMakeBorder(output_img, top=20, left=20, right=20, bottom=20, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])
    rgbimage = Image.fromarray(output_img.astype('uint8'))
    rgbimage = rgbimage.filter(ImageFilter.SMOOTH_MORE)

    return rgbimage


class Ocr:
    def __init__(self):
        self.api = tesserocr.PyTessBaseAPI(lang="mff")
        self.api.SetPageSegMode(tesserocr.PSM.SINGLE_LINE)


    def ocr_using_greyscale(self, image, threshold=200):
        now = datetime.now()
        black_white_image = binarise_greyscale_image(image, threshold)
        self.api.SetImage(black_white_image)

        text = self.api.GetUTF8Text().lower().replace("%", "").replace("\n", "").replace("+", "")
        print(text + "   " + str(datetime.now() - now))
        return text


    def ocr_using_color_similarity(self, image, color=(255,255,255), threshold=120, inverted_colors=False):

        black_white_image = binarise_color_image(image, wanted_rgbtuple=color, threshold=threshold, inverted_colors=inverted_colors)
        # self.api.SetVariable("tessedit_char_whitelist", "1234567890+%.")
        now = datetime.now()
        self.api.SetImage(black_white_image)

        text = self.api.GetUTF8Text().replace("\n", "")
        print(text +"   |" +str(datetime.now()-now))
        return text.lower()


