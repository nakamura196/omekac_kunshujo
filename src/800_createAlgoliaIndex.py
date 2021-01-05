import sys
import urllib
import json
import argparse
import os
import shutil
import glob
import hashlib

data = []

main_path = "../docs/curation/test.json"

with open(main_path) as f:
    curation = json.load(f)

selections = curation["selections"]

for selection in selections:
    members = selection["members"]

    manifest = selection["within"]["@id"]
    label = selection["within"]["label"]

    for member in members:

        member_id = member["@id"]

        hash = hashlib.md5(member_id.encode('utf-8')).hexdigest()

        metadata = member["metadata"]

        tags = []

        for m in metadata:
            if m["label"] == "タグ":
                tags.append(m["value"])

        '''
        member_id_spl = member_id.split("#xywh=")

        canvasId = member_id_spl[0]
        xywh = member_id_spl[1]

        related = "http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest=" + manifest + "&canvas="+canvasId + "&xywh=" + xywh + "&xywh_highlight=border"
        '''

        obj = {
            "objectID": hash,
            "title": member["label"],
            "tags": tags,
            "image": member["thumbnail"],
            "manifest" : manifest,
            "member" : member_id,
            "label" : label
        }

        data.append(obj)

        if len(data) >= 10000:
            break

    if len(data) >= 10000:
        break

opath = "data/algolia.json"

with open(opath, 'w') as outfile:
    json.dump(data, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
