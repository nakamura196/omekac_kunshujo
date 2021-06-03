import sys
import urllib
import json
import argparse
import requests
import os
import shutil
import yaml
import utils

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("type", help='items, item_sets, ..')
parser.add_argument("--isInitOutputDir", help='flag to initialize output directory', default=False)
parser.add_argument("--start", help='page that starts from', default=1)
parser.add_argument("--modified", help='modified that starts from', default=None)

args = parser.parse_args()

target = args.type
modified = args.modified

isInitOutputDir = args.isInitOutputDir == "True"

f = open("../settings.yml", "r+")
settings = yaml.safe_load(f)

output_dir = settings["output_dir"] + "/api/" + target
if isInitOutputDir:
    utils.initDir(output_dir)

'''
dir = "../docs/api/items"
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir, exist_ok=True)
'''

api_url = settings["api_url"]

loop_flg = True
page = int(args.start)

query = ""
if "key" in settings and settings["key"] != None:
    query += "&key="+settings["key"]

if modified:
    query += "&modified_since="+modified

while loop_flg:
    url = api_url + "/"+target+"?page=" + str(
        page) + query

    print(url)

    page += 1

    data = requests.get(url).json()

    if len(data) > 0:
        for i in range(len(data)):
            obj = data[i]

            id = str(obj["id"])

            with open(output_dir+"/"+id+".json", 'w') as outfile:
                json.dump(obj, outfile, ensure_ascii=False,
                            indent=4, sort_keys=True, separators=(',', ': '))

    else:
        loop_flg = False
