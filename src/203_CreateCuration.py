import sys
import urllib
import json
import argparse
import requests
import os
import shutil
import glob


dir = "../docs/oa/collections"

files = sorted(glob.glob(dir+"/*/manifest.json"))

count = 1
count2 = 0
filename = "test.json"
curation_uri = "https://raw.githubusercontent.com/nakamura196/omekac_kunshujo/master/docs/curation/" + filename
curation_label = "Kunshujo"

selections = []

for i in range(0, len(files)):
    file = files[i]
    # print(file)

    with open(file) as f:
        manifest_data = json.load(f)

    canvases = manifest_data["sequences"][0]["canvases"]

    within = {
        "@id" : manifest_data["@id"],
        "@type" : "sc:Manifest",
        "label" : manifest_data["label"]
    }

    members = []

    for canvas in canvases:

        image_api = canvas["images"][0]["resource"]["service"]["@id"]

        otherContent_uri = canvas["otherContent"][0]["@id"]
        otherContent_path = otherContent_uri.replace("https://raw.githubusercontent.com/nakamura196/omekac_kunshujo/master/", "../")

        # print(otherContent_uri)

        if not os.path.exists(otherContent_path):
            continue

        with open(otherContent_path) as f:
            anno_data = json.load(f)

        # print(anno_data)

        resources = anno_data["resources"]

        for j in range(len(resources)):

            resource = resources[j]

            metadata = []

            reses = resource["resource"]
            for res in reses:
                resType = res["@type"]

                if resType == "oa:Tag":
                    resType = "タグ"
                elif resType == "dctypes:Text":
                    resType = "入力者"
                

                metadata.append({
                    "label" : resType,
                    "value" : res["chars"]
                })

            if "on" not in resource:
                continue

            canvas_uri = resource["on"][0]["full"]
            area = resource["on"][0]["selector"]["default"]["value"]

            page = canvas_uri.split("canvas/p")[1]
            
            label = within["label"]

            member = {
                "@id": canvas_uri + "#" + area,
                "@type": "sc:Canvas",
                "label": label + " p." + str(page) + " ["+str(j+1)+"]",
                "description": "",
                "metadata" : metadata,
                "thumbnail" : image_api + "/" + area.split("=")[1]+"/200,/0/default.jpg"
            }

            if "捃拾帖 十九" in label or "捃拾帖 一" in label:
                continue

            members.append(member)

            count2 += 1

    if len(members) == 0:
        continue

    selection = {
        "@id": curation_uri + "/range"+str(count),
        "@type": "sc:Range",
        "label": "Manual curation by IIIF Curation Viewer",
        "members" : members,
        "within" : within
    }

    count += 1

    selections.append(selection)

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

print(count2)
