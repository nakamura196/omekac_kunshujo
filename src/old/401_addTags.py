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
import hashlib

with open("../docs/curation/test.json") as f:
    curation = json.load(f)

selections = curation["selections"]

for selection in selections:
    members = selection["members"]

    

    for member in members:

        metadata = member["metadata"]

        mid = member["@id"]

        id = hashlib.md5(mid.encode('utf-8')).hexdigest()

        file = "../docs/curation/items/"+id+".json"

        if not os.path.exists(file):
            continue
        with open(file) as f:
            item = json.load(f)

        members_ = item["selections"][0]["members"]

        values = []

        for member_ in members_:
            metadata_ = member_["metadata"]
            for m in metadata_:
                if m["label"] == "Tag":
                    value = m["value"]
                    if value not in values:
                        values.append(value)

        for value in values:
            metadata.append({
                "label" : "機械タグ",
                "value" : value
            })

path = "../docs/curation/test.json"
curation["api"] = "https://nakamura196.github.io/omekac_kunshujo/json/api.json"
# curation["api"] = "http://localhost:8008/api.json"

with open(path, 'w') as outfile:
    json.dump(curation, outfile, ensure_ascii=False,
        indent=4, sort_keys=True, separators=(',', ': '))