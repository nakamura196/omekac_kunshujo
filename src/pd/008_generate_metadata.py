# Description: generates a json file that contains the data necessary for the UI
# Example usage:
#   python generate_metadata.py ../data/src/pd_items.json ../js/items/ 5

import json
import math
from pprint import pprint
import re
import sys


INPUT_FILE = "../data/src/curation.json"
OUTPUT_DIR = "../../docs/js/items/"
FILE_COUNT = 5

# init
items = []

# path to curation
curation_path = INPUT_FILE

count = 0

with open(curation_path) as f:
    curation = json.load(f)

    selections = curation["selections"]

    for selection in selections:
        members = selection["members"]

        for member in members:
            items.append([member["thumbnail"], member["label"], member["related"]])

# Write out data
groupSize = int(math.ceil(1.0 * len(items) / FILE_COUNT))
start = 0
end = groupSize
for i in range(FILE_COUNT):
    fileName = OUTPUT_DIR + 'items_'+str(i)+'_'+str(FILE_COUNT)+'.json'
    if i >= FILE_COUNT-1:
        group = items[start:]
    else:
        group = items[start:end]
        start = end
        end += groupSize
    with open(fileName, 'w') as outfile:
        data = {
            'page': i,
            'items': group
        }
        json.dump(data, outfile, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))
    print("Wrote " + str(len(group)) + " lines to " + fileName)
