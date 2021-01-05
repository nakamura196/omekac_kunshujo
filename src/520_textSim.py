import shutil
import requests
import os
import json
import glob
import yaml
import sys
import urllib
import ssl
import csv
import time

import numpy as np
from janome.tokenizer import Tokenizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

path = "../docs/curation/test.json"

labels = []
ids = []
members_ = []

with open(path) as f:
    curation = json.load(f)

    selections = curation["selections"]

    for selection in selections:
        members = selection["members"]

        for member in members:

            members_.append(member)

            label = ""
            metadata = member["metadata"]
            for m in metadata:
                if m["label"] == "タグ":
                    label += m["value"] + " "
            
            labels.append(label)
            ids.append(member["@id"])
 
#わかち書き関数
def wakachi(text):
    
    t = Tokenizer()
    tokens = t.tokenize(text)
    docs=[]
    for token in tokens:
        docs.append(token.surface)
    return docs
 
#文書ベクトル化関数
def vecs_array(documents):
    
 
    docs = np.array(documents)
    vectorizer = TfidfVectorizer(analyzer=wakachi,binary=True,use_idf=False)
    vecs = vectorizer.fit_transform(docs)
    return vecs.toarray()

docs = labels

print("a", len(docs))

#類似度行列作成
cs_array = np.round(cosine_similarity(vecs_array(docs), vecs_array(docs)),3)

size = 20

for i in range(len(cs_array)):

    if i % 10 == 0:
        print(i+1, len(cs_array))

    row = cs_array[i]
    
    member = members_[i]

    uri =  member["@id"]
    id = uri.split("/")[-2]

    arr = sorted(range(len(row)), key=lambda k: row[k], reverse=True)

    texts = []

    for j in range(0, 1 + size):
        index = arr[j]
        id2 = members_[index]["@id"]

        if id2 != uri:
            texts.append(id2)

    member["texts"] = texts    

path = "../docs/curation/test.json"

with open(path, 'w') as outfile:
    json.dump(curation, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))