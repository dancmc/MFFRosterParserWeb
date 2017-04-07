from PIL import Image, ImageColor
import numpy
import math
import tesserocr

ASPECT_RATIO_169 = 16/9
ASPECT_RATIO_1610 = 16/10
ASPECT_RATIO_43 = 4/3


def binarise_greyscale_image(im, threshold=150):
    # in RBG, ndarray contains (row) number of arrays of (column) elements each. Each element is an RBG array
    # in monochrome, ndarray contains (row) number of arrays of (column) ints
    monochrome_image = im.convert('L')  # convert image to monochrome
    # bw_array = numpy.where(numpy.array(monochrome_image) > threshold, 255, 0)
    bw_array = numpy.array(monochrome_image)
    for i in range(len(bw_array)):
        for j in range(len(bw_array[0])):
            if bw_array[i][j] > threshold:
                bw_array[i][j] = 255
            else:
                bw_array[i][j] = 0

    # original_array = numpy.array(im)
    # image2 = numpy.ones((im.size[0], im.size[1], 3), dtype=numpy.int)
    # for i, item in enumerate(original_array):
    #     for j, item2 in enumerate(item):
    #         original_array[i][j] = [255, 255, 255] if (check_similarity(original_array[i][j], 50) else [0, 0, 0]
    # print(image2)

    bw_image = Image.fromarray(bw_array)
    rgbimg = Image.new("RGBA", bw_image.size)
    rgbimg.paste(bw_image)
    return rgbimg


def is_color_similar(color1, color2, similarity):
    threshold = math.pow(similarity, 2) * 3
    # color1 = ImageColor.getrgb(color1)
    color2 = ImageColor.getrgb(color2)
    # lambda acts as a for loop iterating over elements of arguments
    color_diff = sum(tuple(map(lambda x, y: math.pow(x - y, 2), color1, color2)))
    return color_diff <= threshold


def binarise_color_image(im, wantedcolor="white", similarity=None):
    # 6 seconds as well
    # pixels = list(im.getdata())
    # for i in range(len(pixels)):
    #     pixels[i] = (255, 255, 255) if (is_color_similar(pixels[i], "white", 30)) else (0, 0, 0)
    ## newimg = Image.new("RGBA", (im.size[0], im.size[1]))
    # im.putdata(pixels)
    # return im

    # 6+ seconds with Pixel Access
    pixels = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            pixels[i, j] = (255, 255, 255) if (is_color_similar(pixels[i, j], wantedcolor, 30)) else (0, 0, 0)
    return im

    # color_array = numpy.array(im)
    # # image2 = numpy.ones((im.size[0], im.size[1], 3), dtype=numpy.int)
    # for i, rowitem in enumerate(color_array):
    #     for j, columnitem in enumerate(rowitem):
    #         color_array[i][j] = [255, 255, 255] if (is_color_similar(color_array[i][j], "white", 30)) else [0, 0, 0]
    # Image.fromarray(color_array).show()

class Ocr:
    def __init__(self):
        self.api = tesserocr.PyTessBaseAPI(psm=tesserocr.PSM.SINGLE_LINE)


    def ocr_using_greyscale(self, image, threshold=200):
        black_white_image = binarise_greyscale_image(image, threshold)
        self.api.SetImage(black_white_image)

        return self.api.GetUTF8Text().lower().replace("%", "").replace("\n", "")
        # return pytesseract.image_to_string(black_white_image).lower().replace("%", "")


    def ocr_using_color_similarity(self, image, color="white"):
        black_white_image = binarise_color_image(image, color)
        self.api.SetImage(black_white_image)
        return self.api.GetUTF8Text().lower().replace("%", "").replace("\n", "")


