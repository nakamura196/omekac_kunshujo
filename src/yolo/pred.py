import sys
import argparse
from yolo import YOLO, detect_video
from PIL import Image
import glob
import json
import os
import requests
import shutil
import hashlib

prefix = "https://nakamura196.github.io/omekac_kunshujo"

def getCMap(m_data):
    canvases = m_data["sequences"][0]["canvases"]

    map = {}

    for canvas in canvases:
        map[canvas["@id"]] = canvas

    return map

docs_dir = "../../docs"

path = docs_dir + "/curation/test.json"

yolo = YOLO()

count = 0

with open(path) as f:
    curation = json.load(f)

    selections = curation["selections"]

    for selection in selections:
        members = selection["members"]

        manifest = selection["within"]["@id"]

        m_data = requests.get(manifest).json()

        canvas_map = getCMap(m_data)

        for member in members:

            mid = member["@id"]

            canvasId = mid.split("#")[0]

            canvas = canvas_map[canvasId]

            id = hashlib.md5(mid.encode('utf-8')).hexdigest()

            opath = docs_dir + "/curation/items/"+id+".json"
            if os.path.exists(opath):
                continue

            tmp_path = docs_dir + "/files/large/"+id+".jpg"

            try:
                image = Image.open(tmp_path)
            except Exception as e:
                count += 1
                print(e)
                continue
            th_w, th_h = image.size

            org_w = canvas["width"]

            # オリジナルサイズ
            r = org_w / th_w

            try:
                result = yolo.detect_image(image)
            except Exception as e:
                print(e)
                continue

            ##############

            members_ = []

            for obj in result:

                tx = obj["x"]
                ty = obj["y"]
                tw = obj["w"]
                th = obj["h"]

                x = str(int(tx * r))
                y = str(int(ty * r))
                w = str(int(tw * r))
                h = str(int(th * r))

                canvas_uri = canvas["@id"]
                member_uri = canvas_uri + "#xywh=" + x + "," + y + "," + w + "," + h
                chars = obj["label"]

                label = "YOLO v3"

                member = {
                    "@id": member_uri,
                    "@type": "sc:Canvas",
                    "label": chars,
                    "metadata": [
                        {
                            "label": "Method",
                            "value": label
                        },
                        {
                            "label": "Score",
                            "value": str(obj["score"])
                        }
                        ,
                        {
                            "label": "Thumbnail Region",
                            "value": str(tx)+","+str(ty)+","+str(tw)+","+str(th)
                        },
                        {
                            "label": "Tag",
                            "value": chars
                        }
                    ]
                }

                members_.append(member)

            curation = {
                "@context": [
                    "http://iiif.io/api/presentation/2/context.json",
                    "http://codh.rois.ac.jp/iiif/curation/1/context.json"
                ],
                "@id": prefix + "/curation/items/"+id+".json",
                "@type": "cr:Curation",
                "label": "Character List",
                "selections": [
                    {
                        "members" : members_,
                        "within" : selection["within"]
                    }
                ]
            }

            

            with open(opath, 'w') as outfile:
                json.dump(curation, outfile, ensure_ascii=False,
                            indent=4, sort_keys=True, separators=(',', ': '))

print("not exists\t" + str(count))

yolo.close_session()