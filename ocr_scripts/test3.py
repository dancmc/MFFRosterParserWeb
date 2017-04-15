import os

from ..ocr_scripts import ocr as ocr
from PIL import Image

folder="C:/Users/Daniel/Nox_share/Image/training/raw"
save = "C:/Users/Daniel/Nox_share/Image/training/to process"



for filename in os.listdir(folder):
    path = os.path.join(folder, filename)
    screenshot = Image.open(path)

    desiredwidth = 1920
    scale = desiredwidth / screenshot.size[0]
    if screenshot.size[0] < desiredwidth:
        screenshot = screenshot.resize((desiredwidth, int(scale * screenshot.size[1])), Image.NEAREST)
    elif screenshot.size[0] > desiredwidth:
        screenshot.thumbnail((int(screenshot.size[0] * scale), int(screenshot.size[1] * scale)))



    image = ocr.binarise_color_image(screenshot, threshold=135, wanted_rgbtuple=(10, 18, 35), inverted_colors=True)
    image = image.convert("L")
    image.save(os.path.join(save, os.path.splitext(filename)[0]+".tiff"),  dpi=(300., 300.))