import sys
import urllib
import json
import argparse
import requests
import os
import shutil
import glob

import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

dir = "../docs/api/items"

files = sorted(glob.glob(dir+"/*.json"))

files = sorted(files)

filename = "top.json"
curation_uri = "https://raw.githubusercontent.com/nakamura196/omekac_kunshujo/master/docs/curation/" + filename
curation_label = "Kunshujo"

selections_map = {}
uuids = {}

for i in range(0, len(files)):

    file = files[i]

    if i % 100 == 0:
        print(i+1, len(files), file)

    with open(file) as f:
        df = json.load(f)

    element_texts = df["element_texts"]

    manifest_flg = False
    anno_flg = False

    for element_text in element_texts:
        name = element_text["element"]["name"]
        text = element_text["text"]

        if name == "Source":
            manifest_flg = True
            manifest = text

        elif name == "Original @id":
            canvas = text

        elif name == "UUID":
            uuid = text

        elif name == "On Canvas":
            anno_flg = True
            onCanvas = text

        elif name == "Text":
            textValue = cleanhtml(text).strip()

        elif name == "Annotated Region":
            xywh = text

    tags = []
    for tag in df["tags"]:
        tags.append(tag["name"])

    
    if manifest_flg:
        if uuid not in uuids:
            uuids[uuid] = []

        if manifest not in selections_map:
            selections_map[manifest] = {}

        selections_map[manifest][canvas] = uuid

    if anno_flg:

        metadata = [
                {
                    "label" : "入力者",
                    "value" : textValue
                },
                
            ]

        if len(tags) > 0:
            metadata.append({
                    "label" : "タグ",
                    "value" : tags
                })

        member = {
            "xywh" : xywh,
            "metadata" : metadata
        }

        if onCanvas not in uuids:
            uuids[onCanvas] = []

        uuids[onCanvas].append(member)

selections = []

selection_count = 1
for manifest in selections_map:
    canvas_map = selections_map[manifest]

    members = []

    for canvas in canvas_map:
        uuid = canvas_map[canvas]

        annos = uuids[uuid]

        for anno in annos:
            members.append({
                "@id": canvas + "#xywh=" + anno["xywh"],
                "@type": "sc:Canvas",
                # "label": label + " p." + str(page) + " ["+str(j+1)+"]",
                "label": canvas + "#" + anno["xywh"],
                "description": "",
                "metadata" : anno["metadata"],
                # "thumbnail" : image_api + "/" + area.split("=")[1]+"/200,/0/default.jpg"
            })

    if len(members) > 0:
        selections.append({
            "@id": curation_uri + "/range"+str(selection_count),
            "@type": "sc:Range",
            "label": "Manual curation by IIIF Curation Viewer",
            "members" : members,
            "within" : {
                "@id" : manifest,
                "@type" : "sc:Manifest",
                "label" : manifest
            }
        })

        selection_count += 1


curation = {
    "@context": [
        "http://iiif.io/api/presentation/2/context.json",
        "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@type": "cr:Curation",
    "@id": curation_uri,
    "label": curation_label,
    "selections" : selections
}

with open("../docs/curation/" + filename, 'w') as outfile:
    json.dump(curation, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))