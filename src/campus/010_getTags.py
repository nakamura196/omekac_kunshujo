import sys
import urllib
import json
import argparse
import os
import shutil
import glob
import hashlib

tags = {}

main_path = "/Users/nakamurasatoru/git/d_omeka/omekac_kunshujo/docs/curation/top.json"

with open(main_path) as f:
    curation = json.load(f)

selections = curation["selections"]

for selection in selections:
    members = selection["members"]

    for member in members:

        metadata = member["metadata"]

        for m in metadata:
            if m["label"] == "タグ":
                values = m["value"]
                for tag in values:
                    if tag not in tags:
                        tags[tag] = 0

                    tags[tag] += 1

opath = "data/tags.json"

with open(opath, 'w') as outfile:
    json.dump(tags, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
