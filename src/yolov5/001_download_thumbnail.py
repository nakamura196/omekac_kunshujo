import shutil
import requests
import os
import json
import glob
import yaml
import sys
import urllib
import ssl
import csv
import time
import hashlib


def download_img(url, file_name):
    result = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as web_file:
            data = web_file.read()
            with open(file_name, mode='wb') as local_file:
                local_file.write(data)
            print("--- downloaded", id)
    except urllib.error.URLError as e:
        print(id, url, e)
        result = [id, url, e]
    return result

path = "../../docs/curation/top.json"

canvas_images = {}

with open(path) as f:
    curation = json.load(f)

    selections = curation["selections"]

    for i in range(len(selections)):

        selection = selections[i]

        # for selection in selections:
        members = selection["members"]

        manifest = selection["within"]["@id"]

        mid = hashlib.md5(manifest.encode('utf-8')).hexdigest()

        mpath = "../../docs/iiif/" + mid + "/manifest.json"

        if True or not os.path.exists(mpath):
            print(manifest)
            df = requests.get(manifest).json()

            os.makedirs(os.path.dirname(mpath), exist_ok=True)

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

        for j in range(len(members)):
            member = members[j]
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


# print(collection)
