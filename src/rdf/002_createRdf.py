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
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace

sys.path.append('/Users/nakamurasatoru/git/classes')
from rdf import Rdf as rdf

def getGeo(obj, all, subject):
    if "http://www.georss.org/georss/point" in obj:
        labels = obj["http://www.georss.org/georss/point"]
        for label in labels:
            latlng = label["value"].split(" ")

            lat = float(latlng[0])
            lon = float(latlng[1])

            geohash = rdf.geohash(lat, lon)
            
            stmt = (subject, URIRef("http://schema.org/geo"), URIRef(geohash))
            all.add(stmt)

            stmt = (URIRef(geohash), URIRef("http://schema.org/latitude"), Literal(lat))
            all.add(stmt)

            stmt = (URIRef(geohash), URIRef("http://schema.org/longitude"), Literal(lon))
            all.add(stmt)

def getThumbnail(ln, all, subject):
    image_path = "data/wikipedia/" + ln + ".json"
    if os.path.exists(image_path):
        with open(image_path) as f:
            image = json.load(f)

            '''
            if "thumbnail" in image:
                stmt = (subject, URIRef("http://schema.org/image"), URIRef(image["thumbnail"]))
                all.add(stmt)
            '''

            if "original" in image:
                url = image["original"]

                stmt = (subject, URIRef("http://schema.org/associatedMedia"), URIRef(url))
                all.add(stmt)

                ln = url.split("/")[-1]

                thumb = url.replace("/commons/", "/commons/thumb/") + "/200px-" + ln

                stmt = (subject, URIRef("http://schema.org/image"), URIRef(thumb))
                all.add(stmt)

st_path = "/Users/nakamurasatoru/git/d_kunshujo/kunshujo_data/src/data/structured.json"

with open(st_path) as f:
    st = json.load(f)

all = Graph()

for key in st:
    objs = st[key]

    for obj in objs:

        tmp = obj["uri"].split(":")
        prefix = tmp[0]
        suffix = tmp[1]

        subject = URIRef("https://kunshujo.dl.itc.u-tokyo.ac.jp/api/"+prefix+"/"+suffix.replace(" ", "_"))

        if prefix == "chname":
            stmt = (subject, RDF.type, URIRef("https://jpsearch.go.jp/term/type/Agent"))
            all.add(stmt)
        elif prefix == "time":
            stmt = (subject, RDF.type, URIRef("https://jpsearch.go.jp/term/type/Time"))
            all.add(stmt)
        elif prefix == "place":
            stmt = (subject, RDF.type, URIRef("https://jpsearch.go.jp/term/type/Place"))
            all.add(stmt)
        elif prefix == "event":
            stmt = (subject, RDF.type, URIRef("https://jpsearch.go.jp/term/type/Event"))
            all.add(stmt)
        elif prefix == "org":
            stmt = (subject, RDF.type, URIRef("https://jpsearch.go.jp/term/type/Organization"))
            all.add(stmt)
        elif prefix == "keyword":
            stmt = (subject, RDF.type, URIRef("https://jpsearch.go.jp/term/type/Keyword"))
            all.add(stmt)
        elif prefix == "type":
            stmt = (subject, RDF.type, URIRef("https://jpsearch.go.jp/term/type/Type"))
            all.add(stmt)        

        # 実際は機能していない
        if "wiki" not in obj:

            stmt = (subject, RDFS.label, Literal(suffix))
            all.add(stmt)

        else:

            objs = obj["wiki"]

            if len(objs) == 0:
                stmt = (subject, RDFS.label, Literal(suffix))
                all.add(stmt)

            for wiki in objs:

                wiki_url = urllib.parse.unquote(wiki)

                if "www.wikidata" in wiki_url:

                    ln = obj["uri"].split(":")[1]
                    wiki_path = "data/wikidata/"+ln+".json"

                    wiki = {}

                    if os.path.exists(wiki_path):
                        with open(wiki_path) as f:
                            wiki = json.load(f)

                    # sameAs
                    stmt = (subject, URIRef("http://www.w3.org/2002/07/owl#sameAs"), URIRef(wiki_url))
                    all.add(stmt)

                    obj = wiki["entities"][wiki_url.split("/")[-1]]

                    # description
                    if "descriptions" in obj and "ja" in obj["descriptions"]:
                        stmt = (subject, URIRef("http://schema.org/description"), Literal(obj["descriptions"]["ja"]["value"], lang="ja"))
                        all.add(stmt)

                    # label
                    if "labels" in obj and "ja" in obj["labels"]:
                        stmt = (subject, RDFS.label, Literal(obj["labels"]["ja"]["value"]))
                        all.add(stmt)

                else:
                
                    ln = wiki_url.split("/")[-1]

                    getThumbnail(ln, all, subject)
                    

                    db_path = "data/dbpedia_ja/"+ln+".json"
                    wiki_path = "data/wikidata/"+ln+".json"

                    db = {}
                    wiki = {}

                    if os.path.exists(db_path):
                        with open(db_path) as f:
                            db = json.load(f)

                    if os.path.exists(wiki_path):
                        with open(wiki_path) as f:
                            wiki = json.load(f)

                    db_uri = "http://ja.dbpedia.org/resource/"+ln

                    if db_uri not in db:
                        print("当該URIが含まれない" , db_uri)
                        continue

                    obj = db[db_uri]

                    stmt = (subject, URIRef("http://www.w3.org/2002/07/owl#sameAs"), URIRef(db_uri))
                    all.add(stmt)

                    '''
                    if "http://dbpedia.org/ontology/thumbnail" in obj:
                        stmt = (subject, URIRef("http://schema.org/image"), URIRef(obj["http://dbpedia.org/ontology/thumbnail"][0]["value"]))
                        all.add(stmt)
                    '''

                    if "http://www.w3.org/2000/01/rdf-schema#label" in obj:
                        labels = obj["http://www.w3.org/2000/01/rdf-schema#label"]
                        for label in labels:
                            if label["lang"] == "ja":
                                stmt = (subject, RDFS.label, Literal(label["value"]))
                                all.add(stmt)

                    if "http://www.w3.org/2000/01/rdf-schema#comment" in obj:
                        labels = obj["http://www.w3.org/2000/01/rdf-schema#comment"]
                        for label in labels:
                            stmt = (subject, URIRef("http://schema.org/description"), Literal(label["value"], lang=label["lang"]))
                            all.add(stmt)

                    if "http://www.w3.org/2002/07/owl#sameAs" in obj:
                        labels = obj["http://www.w3.org/2002/07/owl#sameAs"]
                        for label in labels:
                            value = label["value"]
                            if "http://dbpedia.org" in value or "http://ja.dbpedia.org" in value or "www.wikidata.org" in value:
                                stmt = (subject, URIRef("http://www.w3.org/2002/07/owl#sameAs"), URIRef(value))
                                all.add(stmt)

                    getGeo(obj, all, subject)

path = "data/all.json"


all.serialize(destination=path, format='json-ld')

####

all.serialize(destination=path.replace(".json", ".rdf"), format='pretty-xml')