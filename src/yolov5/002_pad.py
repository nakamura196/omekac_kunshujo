import shutil
import requests
import os
import json
import glob
from PIL import Image

files = glob.glob("../../docs/files/yolov5/*.jpg")

def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result

for i in range(len(files)):

    file = files[i]

    print(i+1, len(files), file)

    opath = file.replace("yolov5", "yolov5_416x416-black-padding")

    if os.path.exists(opath):
        continue

    im = Image.open(file)

    im_new = expand2square(im, (0,0,0))

    os.makedirs(os.path.dirname(opath), exist_ok=True)

    im_new.save(opath, quality=100)