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

path = "../docs/curation/test.json"

def aaa(manifests, collection):
    manifests2 = []
    if "collections" in collection:
        collections = collection["collections"]

        print(len(collections))

        for i in range(len(collections)):
            collection2 = collections[i]
            manifests2 = aaa(manifests2, collection2)

    elif "manifests" in collection:
        manifests2 = collection["manifests"] 
    
    for j in range(len(manifests2)):
        manifests.append(manifests2[j])

    return manifests

with open(path) as f:
    curation = json.load(f)

    selections = curation["selections"]

    for selection in selections:
        members = selection["members"]

        for member in members:
            thumbnail = member["thumbnail"].replace("/200,/", "/600,/")

            id = member["@id"]
            id = hashlib.md5(id.encode('utf-8')).hexdigest()

            path = "../docs/files/large/"+id+".jpg"

            if not os.path.exists(path):
                download_img(thumbnail, path)


# print(collection)
