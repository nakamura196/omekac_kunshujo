import sys
import urllib
import json
import argparse
import requests
import os
import shutil
import glob

date = "2020-08-07"

URL = "https://diyhistory.org/public/kunshujo/api/items?item_type=1&sort_field=modified&sort_dir=d&modified_since=" + date

prefix_1 = "https://diyhistory.org/public/kunshujo"
prefix_2 = "../docs"
prefix_3 = "https://raw.githubusercontent.com/nakamura196/omekac_kunshujo/master/docs"

def get(data_json, data_url):
    # data_json = requests.get(data_url).json()

    data_path = data_url.replace(prefix_1, prefix_2)

    os.makedirs(os.path.dirname(data_path), exist_ok=True)

    with open(data_path, 'w') as outfile:
        json.dump(data_json, outfile, ensure_ascii=False,
                    indent=4, sort_keys=True, separators=(',', ': '))



dir = "../docs/api/collections"

files = glob.glob(dir+"/*.json")

top_url = "https://diyhistory.org/public/kunshujo/oa/top.json"

top_json = requests.get(top_url).json()

top_json["@id"] = top_json["@id"].replace(prefix_1, prefix_3)

collections = top_json["collections"]

for collection in collections:
    collection_url = collection["@id"]

    print(collection_url)

    collection_json = requests.get(collection_url).json()
    manifests = collection_json["manifests"]

    for manifest in manifests:
        manifest_url = manifest["@id"]

        print(manifest_url)

        manifest_json = requests.get(manifest_url).json()

        canvases = manifest_json["sequences"][0]["canvases"]

        for canvas in canvases:
            otherContent_url = canvas["otherContent"][0]["@id"]

            data_path = otherContent_url.replace(prefix_1, prefix_2)

            anno_id = int(otherContent_url.split("/")[-2])

            if anno_id < 1353:
                continue

            if os.path.exists(data_path):
                continue

            print("***", otherContent_url, data_path)
            
            canvas["otherContent"][0]["@id"] = canvas["otherContent"][0]["@id"].replace(prefix_1, prefix_3)

            # --------

            otherContent_json = requests.get(otherContent_url).json()
            otherContent_json["@id"] = otherContent_json["@id"].replace(prefix_1, prefix_3)

            resources = otherContent_json["resources"]

            if len(resources) == 0:
                continue

            ons = resources[0]["on"]

            for on in ons:
                on["within"]["@id"] = on["within"]["@id"].replace(prefix_1, prefix_3)

            get(otherContent_json, otherContent_url)

        manifest_json["@id"] = manifest_json["@id"].replace(prefix_1, prefix_3)
        get(manifest_json, manifest_url)

        # --------

        manifest["@id"] = manifest["@id"].replace(prefix_1, prefix_3)

    
    collection_json["@id"] = collection_json["@id"].replace(prefix_1, prefix_3)
    

    get(collection_json, collection_url)

    # -----------

    collection["@id"] = collection["@id"].replace(prefix_1, prefix_3)

get(top_json, top_url)


