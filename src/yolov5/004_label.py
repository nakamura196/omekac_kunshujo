import shutil
import requests
import os
import json
import glob
# import yaml
import sys
import urllib
import ssl
import csv
import time
import hashlib

path = "../../docs/curation/top.json"

canvas_map = {}

with open(path) as f:
    curation = json.load(f)

    selections = curation["selections"]

    for i in range(len(selections)):

        selection = selections[i]

        # for selection in selections:
        members = selection["members"]

        ###########

        manifest = selection["within"]["@id"]

        mid = hashlib.md5(manifest.encode('utf-8')).hexdigest()

        mpath = "../../docs/iiif/" + mid + "/manifest.json"

        if not os.path.exists(mpath):
            df = requests.get(manifest).json()

            os.makedirs(os.dirname(mpath), exist_ok=True)

            with open(mpath, 'w') as outfile:
                json.dump(df, outfile, ensure_ascii=False,
                            indent=4, sort_keys=True, separators=(',', ': '))

        with open(mpath) as f:
            mdata = json.load(f)

        images = {}

        canvases = mdata["sequences"][0]["canvases"]
        for canvas2 in canvases:
            images[canvas2["@id"]] = {
                "width" : canvas2["width"],
                "height" : canvas2["height"],
                "image" : canvas2["images"][0]["resource"]["service"]["@id"]
            }

        ###########

        for j in range(len(members)):
            member = members[j]

            spl = member["@id"].split("#xywh=")

            xywh = spl[1].split(",")

            x = int(xywh[0])
            y = int(xywh[1])
            w = int(xywh[2])
            h = int(xywh[3])

            img = images[spl[0]]

            width = img["width"]
            height = img["height"]

            line = max(width, height)

            # r = 416 / line

            # print(r)

            x2 = x + (line - width) / 2 # 補完
            y2 = y + (line - height) / 2

            x_center = (x2 + w / 2) / line
            y_center = (y2 + h / 2) / line
            w2 = w / line
            h2 = h / line

            row = "{} {} {} {} {}".format(0, x_center, y_center, w2, h2)

            # thumbnail = img["image"] + "/full/!416,416/0/default.jpg"

            id = spl[0] # member["@id"]
            id = hashlib.md5(id.encode('utf-8')).hexdigest()

            if id not in canvas_map:
                canvas_map[id] = []

            canvas_map[id].append(row)

            '''
            # for member in members:
            # thumbnail = member["thumbnail"]

            spl = member["@id"].split("#xywh=")

            img = images[spl[0]]

            # size = "416," if img["width"] < img["height"] else ",416"

            thumbnail = img["image"] + "/full/!416,416/0/default.jpg"

            id = spl[0] # member["@id"]
            id = hashlib.md5(id.encode('utf-8')).hexdigest()

            path = "../../docs/files/yolov5/"+id+".jpg"

            if not os.path.exists(path):
                print(i, len(selections), j, len(members))
                download_img(thumbnail, path)
            '''

for id in canvas_map:
    path = "../../docs/files/labels/" + id + ".txt"

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as f:
        for item in canvas_map[id]:
            f.write("%s\n" % item)

# print(collection)
