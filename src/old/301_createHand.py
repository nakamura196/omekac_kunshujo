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

import csv

def test(value, subjects, map):
    for term in map:
        if term in value:
            id = map[term]["id"]
            if id not in subjects:
                subjects[id] =  map[term]["label"]

    return subjects

map = {}

with open('data/map.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        map[row[0]] = {
            "label" : row[1],
            "id" : row[2]
        }

with open("../docs/curation/test.json") as f:
    curation = json.load(f)

'''
with open("../docs/iiif/top.json") as f:
    collection = json.load(f)
'''
results = []

def aaa(manifests, collection):
    manifests2 = []
    if "collections" in collection:
        collections = collection["collections"]

        for i in range(len(collections)):
            collection2 = collections[i]
            manifests2 = aaa(manifests2, collection2)

    elif "manifests" in collection:
        manifests2 = collection["manifests"] 
    
    for j in range(len(manifests2)):
        manifests.append(manifests2[j])

    return manifests

'''
manifests = aaa([], collection)

for manifest in manifests:

    subjects = {}

    mlabel = manifest["label"]
    subjects = test(mlabel, subjects, map)

    metadata = manifest["metadata"]

    for m in metadata:
        subjects = test(m["value"], subjects, map)

    subjectArr = []
    for id in subjects:
        subjectArr.append({
        "@id": id,
        "o:label" : subjects[id]
      })

    result = {
        "@context": "https://diyhistory.org/public/omekas3a/api-context",
        "@id": manifest["@id"],
        "schema:subject": subjectArr
    }

    if len(subjectArr) > 0:
        results.append(result)

'''

selections = curation["selections"]

for selection in selections:
    members = selection["members"]

    

    for member in members:

        subjects = {}

        for m in member["metadata"]:
            subjects = test(m["value"], subjects, map)

        subjectArr = []
        for id in subjects:
            subjectArr.append({
            "@id": id,
            "o:label" : subjects[id]
        })

        result = {
            "@context": "https://diyhistory.org/public/omekas3a/api-context",
            "@id": member["@id"],
            "schema:subject": subjectArr
        }

        if len(subjectArr) > 0:
            results.append(result)
        
    
path = "data/hand2.json"

with open(path, 'w') as outfile:
    json.dump(results, outfile, ensure_ascii=False,
        indent=4, sort_keys=True, separators=(',', ': '))