from PIL import Image, ImageColor
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


def binarise_greyscale_image(im, threshold=150):
    # in RBG, 3d array contains (row) number of arrays of (column) elements each. Each element is an RBG array
    monochrome_image = im.convert('L')
    bw_array = numpy.where(numpy.array(monochrome_image, numpy.uint8) > threshold, 255, 0)

    # Method 1a
    # rgb_array = numpy.array([numpy.array((y, y, y), numpy.uint8) for x in bw_array for y in x])
    # rgb_array = rgb_array.reshape((bw_array.shape[0], bw_array.shape[1], 3))

    # Method 1b : same speed, but horrible readability
    # rgb_array = numpy.array(list(map(lambda x:numpy.array(list(map(lambda y:numpy.array((y,y,y)),x))), bw_array)))
    # rgb_array = rgb_array.reshape((bw_array.shape[0], bw_array.shape[1], 3))

    # Method 2 (slowest)
    # bw_array = numpy.array(monochrome_image)
    # rgb_array = numpy.empty((bw_array.shape[0], bw_array.shape[1], 3))
    # for i in range(bw_array.shape[0]):
    #     for j in range(bw_array.shape[1]):
    #         rgb_array[i][j] = [255, 255, 255] if bw_array[i][j] > 100 else [0, 0, 0]

    # Optional : applying erosion
    # bgr_array = reverse_numpy(rgb_array)
    # kernel = numpy.ones((2, 2), numpy.uint8)
    # rgb_array = reverse_numpy(cv2.erode(bgr_array, kernel, iterations=1))
    # rgbimg = Image.fromarray(rgb_array.astype('uint8'))

    # Method 3 (fastest)
    bw_image = Image.fromarray(bw_array.astype('uint8'))
    rgbimg = Image.new("RGB", bw_image.size)
    rgbimg.paste(bw_image)

    # Optional : erosion using cv2
    # bgr_array = PIL_to_opencv(rgbimg)
    # kernel = numpy.ones((1, 1), numpy.uint8)
    # rgb_array = reverse_numpy(cv2.erode(bgr_array, kernel, iterations=1))
    # rgbimg = Image.fromarray(rgb_array.astype('uint8'))
    # rgbimg.show()

    return rgbimg

def binarise_color_image(im, wanted_rgbtuple=(255,255,255), threshold = 20, inverted_colors=False, erode=False):
    # Method 1 : 6 seconds as well
    # pixels = list(im.getdata())
    # for i in range(len(pixels)):
    #     pixels[i] = (255, 255, 255) if (is_color_similar(pixels[i], "white", 30)) else (0, 0, 0)
    # # newimg = Image.new("RGBA", (im.size[0], im.size[1]))
    # im.putdata(pixels)
    # return im

    # Method 2: Pixel Access, 6+ seconds
    # pixels = im.load()
    # for i in range(im.size[0]):
    #     for j in range(im.size[1]):
    #         pixels[i, j] = (255, 255, 255) if (is_color_similar(pixels[i, j], wantedcolor, 30)) else (0, 0, 0)
    # return im

    # Method 3:
    # color_array = numpy.array(im)
    # image2 = numpy.ones((im.size[0], im.size[1], 3), dtype=numpy.int)
    # for i, rowitem in enumerate(color_array):
    #     for j, columnitem in enumerate(rowitem):
    #         color_array[i][j] = [255, 255, 255] if (is_color_similar(color_array[i][j], "white", 30)) else [0, 0, 0]
    # return Image.fromarray(color_array.astype('uint8'))

    # Method 4: color thresholding (fastest)
    bgr_array = PIL_to_opencv(im)

    if(erode):
        bgr_array = cv2.resize(bgr_array, None, fx=1.1, fy=1.1, interpolation=cv2.INTER_CUBIC)
        pass


    lower_color = numpy.array([max(0, x-threshold) for x in wanted_rgbtuple])[::-1]
    upper_color = numpy.array([min(255, x + threshold) for x in wanted_rgbtuple])[::-1]
    mask = cv2.inRange(bgr_array, lower_color, upper_color)

    # mask a blank image instead of original - get a binarised image instead of original color
    output_img = bgr_array.copy()
    output_img = output_img.astype(numpy.uint8)
    output_img[:] = 255
    output_img = cv2.bitwise_and(output_img, output_img, mask=mask)

    # rgb_array = reverse_numpy(output_img)
    # rgb_image = Image.fromarray(rgb_array.astype('uint8'))
    # rgbimage = Image.new("RGB", rgb_image.size)
    # rgbimage.paste(rgb_image)
    # # rgb_image.show()

    # usually wanted_rgbtuple should be text color. if background color retained, invert flag should be set
    if(inverted_colors):
        output_img = numpy.where(output_img[:,:,:]==0, 255, 0, )
        output_img = output_img.astype(numpy.uint8)




    # # erode text if flag set. text must be white

    if(erode):
        kernel = numpy.ones((3, 3), numpy.uint8)
        # output_img = cv2.GaussianBlur(output_img, (7, 7), 0)
        output_img = cv2.erode(output_img,kernel, iterations=1)
        output_img = cv2.dilate(output_img, kernel, iterations=1)
    else :
        kernel = numpy.ones((3, 3), numpy.uint8)
        output_img = cv2.dilate(output_img, kernel, iterations=1)

    # opencv_to_PIL(output_img).show()

    rgb_array = reverse_numpy(output_img)
    rgb_image = Image.fromarray(rgb_array.astype('uint8'))
    rgbimage = Image.new("RGB", rgb_image.size)
    rgbimage.paste(rgb_image)
    # rgb_image.show()

    return rgbimage


class Ocr:
    def __init__(self):
        self.api = tesserocr.PyTessBaseAPI(psm=tesserocr.PSM.SINGLE_LINE)


    def ocr_using_greyscale(self, image, threshold=200):
        now = datetime.now()
        black_white_image = binarise_greyscale_image(image, threshold)
        self.api.SetImage(black_white_image)

        text = self.api.GetUTF8Text().lower().replace("%", "").replace("\n", "")
        print(text + "   " + str(datetime.now() - now))
        return text


    def ocr_using_color_similarity(self, image, color=(255,255,255), threshold = 20, inverted_colors=False, erode=False):
        now = datetime.now()
        black_white_image = binarise_color_image(image, color, threshold, inverted_colors, erode)
        # self.api.SetVariable("tessedit_char_whitelist", "1234567890+%.")
        self.api.SetImage(black_white_image)

        text = self.api.GetUTF8Text().lower().replace("%", "").replace("\n", "")
        print(text +"   " +str(datetime.now()-now))
        return text


