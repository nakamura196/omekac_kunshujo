import shutil
import os
import json
import glob
import yaml
import sys
import urllib
import ssl
import csv
import time
import requests
import json
import csv

st_path = "/Users/nakamurasatoru/git/d_kunshujo/kunshujo_data/src/data/structured.json"

with open(st_path) as f:
    st = json.load(f)

for key in st:
    objs = st[key]

    for obj in objs:
        # print(obj)
        wikis = obj["wiki"]

        for wiki in wikis:
            map = {}

            ln = wiki.split("/")[-1]
            path = "data/wikipedia/{}.json".format(ln)

            if os.path.exists(path):
                continue

            types = ["original", "thumbnail"]

            for type in types:
                api = "https://ja.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop={}&titles={}".format(type, ln)
                df = requests.get(api).json()
                pages = df["query"]["pages"]

                for key in pages:
                    if type in pages[key]:
                        url = pages[key][type]["source"]
                        map[type] = url
            
            with open(path, 'w') as outfile:
                json.dump(map, outfile, ensure_ascii=False,
                    indent=4, sort_keys=True, separators=(',', ': '))
