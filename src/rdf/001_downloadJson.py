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

    if os.path.exists(opath):
        return

    dirname = os.path.dirname(opath)
    os.makedirs(dirname, exist_ok=True)

    try:
        result = requests.get(url).json()

        with open(opath, 'w') as outfile:
            json.dump(result, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
    
    except Exception as e:
        print("Err", url)

st_path = "/Users/nakamurasatoru/git/d_kunshujo/kunshujo_data/src/data/structured.json"

with open(st_path) as f:
    st = json.load(f)

for key in st:
    objs = st[key]

    for obj in objs:

        if "wiki" in obj:
            wikis = obj["wiki"]

            for wiki in wikis:
                wiki = urllib.parse.unquote(wiki)
                print(wiki)

                if "www.wikidata" in wiki:

                    ln = obj["uri"].split(":")[1]

                    wikidata = wiki+".json"
                    print(wikidata)
                    opath = "data/wikidata/"+ln+".json"
                    dwn(wikidata, opath)
                else:
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

                            uri = "http://ja.dbpedia.org/resource/"+ln

                            if uri not in df:
                                continue

                            obj = df[uri]

                            if "http://www.w3.org/2002/07/owl#sameAs" in obj:

                                sames = obj["http://www.w3.org/2002/07/owl#sameAs"]

                                for s in sames:
                                    if "www.wikidata.org" in s["value"]:
                                        wikidata = s["value"]+".json"
                                        opath = "data/wikidata/"+ln+".json"
                                        dwn(wikidata, opath)

        elif "wikidata" in obj:
            values = obj["wikidata"]
            for value in values:
                ln = value.split("/")[-1]
                opath = "data/wikidata2/"+ln+".json"
                dwn(value, opath)
                    