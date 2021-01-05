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

with open("data/hand2.json") as f:
    hand = json.load(f)

hand_map = {}
for obj in hand:
    manifest_id = obj["@id"]
    hand_map[manifest_id] = obj

with open("../docs/curation/test.json") as f:
    curation = json.load(f)

selections = curation["selections"]

for selection in selections:
    members = selection["members"]

    

    for member in members:

        metadata = member["metadata"]

        m_id = member["@id"]
        if m_id in hand_map:
            hand = hand_map[m_id]

            for uri in hand:
                print(uri)
                values = hand[uri]
                for value in values:
                    if "@id" in value:
                        id = value["@id"]
                        label = value["o:label"]
                        # print(uri, "@id", value["@id"])
                        metadata.append({
                            "label" : uri, #labels[uri],
                            "value" : label,
                            "property" : uri,
                            "uri" : id
                        })
                    elif "@value" in value:
                        # print(uri, "@value", value["@value"])
                        label = value["@value"]
                        metadata.append({
                            "label" : uri, #labels[uri],
                            "value" : label,
                            "property" : uri
                        })


path = "../docs/curation/test.json"
curation["api"] = "https://nakamura196.github.io/omekac_kunshujo/json/api.json"
# curation["api"] = "http://localhost:8008/api.json"

with open(path, 'w') as outfile:
    json.dump(curation, outfile, ensure_ascii=False,
        indent=4, sort_keys=True, separators=(',', ': '))