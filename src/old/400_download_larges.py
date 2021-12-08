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
            print("downloaded", url)
    except urllib.error.URLError as e:
        print("error", url, e)
        result = [url, e]
    return result

path = "../../docs/curation/top.json"

with open(path) as f:
    curation = json.load(f)

    targets = []

    selections = curation["selections"]

    for selection in selections:
        members = selection["members"]

        for member in members:
            thumbnail = member["thumbnail"].replace("/200,/", "/600,/")

            id = member["@id"]
            id = hashlib.md5(id.encode('utf-8')).hexdigest()

            path = "../../docs/files/large/"+id+".jpg"

            if not os.path.exists(path):
                # download_img(thumbnail, path)
                targets.append({
                    "url": thumbnail,
                    "path": path
                })

    for i in range(len(targets)):
        if i % 100 == 0:
            print(i+1, len(targets))

        target = targets[i]

        download_img(target["url"], target["path"])