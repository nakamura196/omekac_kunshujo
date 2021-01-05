import sys
import urllib
import json
import argparse
import os
import shutil
import glob
import hashlib

data = []

def n_gram(target, n):
  # 基準を1文字(単語)ずつ ずらしながらn文字分抜き出す
  return [ target[idx:idx + n] for idx in range(len(target) - n + 1)]

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

        text = ""
        for tag in tags:
            text += tag + " "
        list = n_gram(text, 2)
        
        tokenMap = {}
        for l in list:
            tokenMap[l] = True

        '''
        member_id_spl = member_id.split("#xywh=")

        canvasId = member_id_spl[0]
        xywh = member_id_spl[1]

        related = "http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest=" + manifest + "&canvas="+canvasId + "&xywh=" + xywh + "&xywh_highlight=border"
        '''

        obj = {
            "id": hash,
            "title": member["label"],
            "tags": tags,
            "tokenMap" : tokenMap,
            "image": member["thumbnail"],
            "manifest" : manifest,
            "member" : member_id,
            "label" : label
        }

        data.append(obj)

opath = "data/firestore.json"

firestore = {
    "items" : data
}

with open(opath, 'w') as outfile:
    json.dump(firestore, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
