import shutil
import requests
import os
import json
import glob
from PIL import Image
import random
import shutil

from sklearn.model_selection import train_test_split

files = glob.glob("../../docs/files/yolov5_416x416-black-padding/*.jpg")

'''
total = len(files)

valid_size = int(total * 0.2)
test_size = int(total * 0.1)

rand_list = random.sample(files, valid_size + test_size)
print(rand_list)
'''

X_train, X_valid = train_test_split(files, random_state=1, train_size=0.8)
X_train, X_test = train_test_split(X_train, random_state=1, train_size=7/8)

map = {
    "valid" : X_valid,
    "train" : X_train,
    "test" : X_test
}

print("total", len(files))




for key in map:
    files = map[key]

    shutil.rmtree("../../docs/files/yolov5_416x416-black-padding.v2/" + key)

    for file in files:
        opath = file.replace("yolov5_416x416-black-padding", "yolov5_416x416-black-padding.v2/{}/images".format(key))
        os.makedirs(os.path.dirname(opath), exist_ok=True)
        shutil.copy(file, opath)

        filename = os.path.basename(file).replace(".jpg", ".txt")
        label_path = "../../docs/files/labels/" + filename
        label_o_path = "../../docs/files/yolov5_416x416-black-padding.v2/" + key + "/labels/" + filename

        os.makedirs(os.path.dirname(label_o_path), exist_ok=True)
        shutil.copy(label_path, label_o_path)

    print(key, len(files))

'''

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

'''