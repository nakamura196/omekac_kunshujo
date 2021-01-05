import sys
import urllib
import json
import argparse
import os
import shutil
import glob

selections_ = []

files2 = glob.glob("/Users/nakamurasatoru/git/d_utda/kunshujo-i/docs/curation_m/manual/*.json")

for file in files2:
    with open(file) as f:
        curation_data = json.load(f)

    selection = curation_data["selections"][0]
    selections_.append(selection)

main_path = "../docs/curation/test.json"

with open(main_path) as f:
    curation = json.load(f)

selections = curation["selections"]

for selection in selections:
    selections_.append(selection)

selections = selections_
curation["selections"] = selections_

with open(main_path, 'w') as outfile:
    json.dump(curation, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
