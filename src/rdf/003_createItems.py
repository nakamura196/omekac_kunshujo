import elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
import json
import hashlib

from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace

main_path = "/Users/nakamurasatoru/git/d_kunshujo/kunshujo/src/data/es.json"

with open(main_path) as f:
    curation = json.load(f)

# print(curation)

all = Graph()

for obj in curation:
    source = obj["_source"]

    subject = URIRef("https://kunshujo.web.app/api/data/"+obj["_id"])

    stmt = (subject, RDF.type, URIRef("https://jpsearch.go.jp/term/type/Item"))
    all.add(stmt)

    stmt = (subject, RDFS.label, Literal(source["_label"][0]))
    all.add(stmt)

    fields = {
        "agentials" : {
            "prefix" : "chname",
            "uri" : "https://jpsearch.go.jp/term/property#agential"
        },
        "places" : {
            "prefix" : "place",
            "uri" : "http://schema.org/spatial"
        },
        "times" : {
            "prefix" : "time",
            "uri" : "http://schema.org/temporal"
        },
        "keywords" : {
            "prefix" : "keyword",
            "uri" : "http://schema.org/about"
        },
        "orgs" : {
            "prefix" : "org",
            "uri" : "https://jpsearch.go.jp/term/property#organization"
        },
        "events" : {
            "prefix" : "event",
            "uri" : "https://jpsearch.go.jp/term/property#event"
        }
    }

    for key in fields:
        if key not in source:
            continue
        arr = source[key]
        for value in arr:
            o = "https://kunshujo.web.app/api/"+fields[key]["prefix"]+"/"+value
            stmt = (subject, URIRef(fields[key]["uri"]), URIRef(o))
            all.add(stmt)

    stmt = (subject, URIRef("http://schema.org/image"), URIRef(source["_thumbnail"][0]))
    all.add(stmt)

    for tag in source["tags"]:
        stmt = (subject, URIRef("http://schema.org/description"), Literal(tag))
        all.add(stmt)

    stmt = (subject, URIRef("http://schema.org/relatedLink"), URIRef("https://kunshujo.web.app/item/"+obj["_id"]))
    all.add(stmt)

    stmt = (subject, URIRef("https://jpsearch.go.jp/term/property#sourceData"), URIRef("https://search:lqtia2ngm63yi5tam7ewxjvqhogjem82@gimli-eu-west-1.searchly.com/main/_doc/"+obj["_id"]))
    all.add(stmt)

path = "data/items.json"
all.serialize(destination=path.replace(".json", ".rdf"), format='pretty-xml')
