import sys
import urllib
import json
import argparse
import requests
import os
import shutil
import yaml
import glob

path = "../../docs/api/items/*.json"

files = glob.glob(path)

map = {}

for i in range(len(files)):
    file = files[i]
    
    with open(file) as f:
        item = json.load(f)

        if item["item_type"] != None and item["item_type"]["id"] == 1:
            print(file)

            added = item["added"]

            spl = added.split("-")

            year = spl[0]
            month = spl[1]

            yearAndMonth = year + "-" + month

            if yearAndMonth not in map:
                map[yearAndMonth] = 0
            
            map[yearAndMonth] += 1

rows = []
rows.append(["yearAndMonth", "count"])

for yearAndMonth in map:
    rows.append([yearAndMonth, map[yearAndMonth]])

import csv

with open('data.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(rows) # 2次元配列も書き込める