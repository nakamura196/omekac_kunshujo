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
import requests
import json
import csv

map = {}
dbpedia_uris = {}

with open('data/map.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        map[row[2]] = {
            "label" : row[1],
            "id" : row[2]
        }

        dbpedia_uris["http://ja.dbpedia.org/resource/"+row[1]] = row[2]

path = "../docs/json/api.json"
with open(path) as f:
    results = json.load(f)

results = []

uris = []

for result in results:
    uris.append(result["@id"])

count = 0
for wikidata_uri in map:
    
    count += 1

    print(wikidata_uri, count, len(map))

    if wikidata_uri in uris:
        "continue w"
        continue

    try:
        wikidata = requests.get(wikidata_uri+".json").json()

        data = wikidata["entities"][wikidata_uri.split("/")[-1]]
        labels = data["labels"]

        label_ja = labels["ja"]["value"] if "ja" in labels else ""
        label_en = labels["en"]["value"] if "en" in labels else ""

        

        descriptions = data["descriptions"]
        description_ja = descriptions["ja"]["value"] if "ja" in descriptions else ""
        description_en = labels["en"]["value"] if "en" in descriptions else ""
    except Exception as e:
        print(e)
        # continue
    # print(wikidata)
    

    

    # -----

    

    uri = "http://ja.dbpedia.org/resource/" + map[wikidata_uri]["label"]
    try:
        dbpedia = requests.get(uri.replace("/resource/", "/data/")+".json").json()
    except Exception as e:
        print("con 2", e)
        # continue

    if uri not in dbpedia:
        print("con 3")
        continue

    data = dbpedia[uri]
    # print(data)

    if label_ja == "" and "http://www.w3.org/2000/01/rdf-schema#label" in data:
        label_ja = data["http://www.w3.org/2000/01/rdf-schema#label"][0]["value"]

    if description_ja == "" and "http://www.w3.org/2000/01/rdf-schema#comment" in data:
        description_ja = data["http://www.w3.org/2000/01/rdf-schema#comment"][0]["value"]


    # -----

    if label_en != "" and label_ja == "":
        label_ja = label_en

    if label_ja == "":
        label_ja = "No Title"

    if description_en != "" and description_ja == "":
        description_ja = description_en

    # -----

    
    thumbnail = ""
    if "http://dbpedia.org/ontology/thumbnail" in data:
        thumbnail = data["http://dbpedia.org/ontology/thumbnail"][0]["value"]


    result = {
        "@context": "https://diyhistory.org/public/omekas3a/api-context",
        "@id": wikidata_uri,
        "rdfs:label": [
            { 
                "@value" : label_ja
            }
        ]
    }

    if label_en != "":
        result["schema:name"] = [
            {
                "@value" : label_en,
                "@language": "en"
            }
        ]

    if description_ja != "":
        result["schema:description"] = [
            {
                 "@value" : description_ja
            }
        ]

    if thumbnail != "":
        result["schema:image"] = [
            {
                 "@id" : thumbnail
            }
        ]
    
    for key in data:
        values = data[key]
        for value in values:
            if value["type"] == "uri":
                id = value["value"]
                if id in dbpedia_uris:
                    property = key.replace("http://dbpedia.org/ontology/", "dbo:").replace("http://ja.dbpedia.org/property/", "dbp:")

                    if property not in result:
                        result[property] = []

                    result[property].append({
                        "@id" : dbpedia_uris[id]
                    })

    
    results.append(result)

with open(path, 'w') as outfile:
    json.dump(results, outfile, ensure_ascii=False,
        indent=4, sort_keys=True, separators=(',', ': '))