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

def dwn(url, opath):
    if not os.path.exists(opath):
        dirname = os.path.dirname(opath)
        os.makedirs(dirname, exist_ok=True)

    try:
        result = requests.get(url).json()

        with open(opath, 'w') as outfile:
            json.dump(result, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

        
        
    except Exception as e:
        print("Err", url)

st_path = "/Users/nakamurasatoru/git/d_omeka/omekac_kunshujo/src/campus/data/structured.json"

with open(st_path) as f:
    st = json.load(f)

for key in st:
    obj = st[key]
    if "wiki" in obj:
        wiki = urllib.parse.unquote(obj["wiki"])
        print(wiki)
        ln = wiki.split("/")[-1]

        dbpedia_ja = "http://ja.dbpedia.org/data/" + ln + ".json"

        opath = "data/dbpedia_ja/"+ln+".json"

        if not os.path.exists(opath):
            dirname = os.path.dirname(opath)
            os.makedirs(dirname, exist_ok=True)

            try:
                result = requests.get(dbpedia_ja).json()

                with open(opath, 'w') as outfile:
                    json.dump(result, outfile, ensure_ascii=False,
                        indent=4, sort_keys=True, separators=(',', ': '))

                
                
            except Exception as e:
                print("Err", dbpedia_ja)

        if os.path.exists(opath):
            with open(opath) as f:
                df = json.load(f)

                obj = df["http://ja.dbpedia.org/resource/"+ln]

                if "http://www.w3.org/2002/07/owl#sameAs" in obj:

                    sames = obj["http://www.w3.org/2002/07/owl#sameAs"]

                    for s in sames:
                        if "www.wikidata.org" in s["value"]:
                            wikidata = s["value"]+".json"
                            opath = "data/wikidata/"+ln+".json"
                            dwn(wikidata, opath)

            