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

with open("data/hand2.json") as f:
    hand = json.load(f)

hand_map = {}
for obj in hand:
    manifest_id = obj["@id"]
    hand_map[manifest_id] = obj

with open("../docs/iiif/top.json") as f:
    collection = json.load(f)

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

manifests = aaa([], collection)

'''
labels = {
    "schema:creator" : "Creator",
    "schema:about" : "About",
    "schema:temporal" : "Temporal"
}
'''

for manifest in manifests:

    metadata = manifest["metadata"]

    manifest_id = manifest["@id"]
    if manifest_id in hand_map:
        hand = hand_map[manifest_id]

        for uri in hand:
            print(uri)
            values = hand[uri]
            for value in values:
                if "@id" in value:
                    id = value["@id"]
                    label = value["o:label"]
                    # print(uri, "@id", value["@id"])
                    metadata.append({
                        "label" : uri, #labels[uri],
                        "value" : label,
                        "property" : uri,
                        "uri" : id
                    })
                elif "@value" in value:
                    # print(uri, "@value", value["@value"])
                    label = value["@value"]
                    metadata.append({
                        "label" : uri, #labels[uri],
                        "value" : label,
                        "property" : uri
                    })


path = "../docs/iiif/top.json"
collection["api"] = "https://nakamura196.github.io/nishikie/json/api.json"
# collection["api"] = "http://localhost:8008/api.json"

with open(path, 'w') as outfile:
    json.dump(collection, outfile, ensure_ascii=False,
        indent=4, sort_keys=True, separators=(',', ': '))