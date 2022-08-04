path = "data/all copy.json"

import json
import os
import bs4
from tqdm import tqdm

with open(path) as f:
    df = json.load(f)

    items = []

    for item in tqdm(df):
        items.append(item)
        ln = item["@id"].split("/")[-1]



        '''
        if ln != "パリ":
            continue
        '''

        if "http://schema.org/geo" not in item and "@type" in item and item["@type"][0] == "https://jpsearch.go.jp/term/type/Place":
            wiki = f"data/wikipedia/{ln}.html"
            if os.path.exists(wiki):
                soup = bs4.BeautifulSoup(open(wiki), 'html.parser')
                geo = soup.find(class_="geo")
                if geo:
                    geo = geo.text.split("; ")
                    # print(geo)

                    geohash = f"http://geohash.org/{geo[0]},{geo[1]}"

                    item["http://schema.org/geo"] = [
                        {
                            "@id": geohash
                        }
                    ]

                    items.append({
                        "@id": geohash,
                        "http://schema.org/latitude": [
                        {
                            "@value": float(geo[0])
                        }
                        ],
                        "http://schema.org/longitude": [
                        {
                            "@value": float(geo[1])
                        }
                        ]
                    })

        if "http://schema.org/image" not in item:
            wiki = f"data/media/{ln}.json"
            if os.path.exists(wiki):
                # print(ln)
                with open(wiki) as f:
                    df2 = json.load(f)

                pages = df2["query"]["pages"]

                if "-1" in pages:
                    continue

                item = pages[list(pages.keys())[0]]

                if "thumbnail" not in item:
                    continue

                url = item["thumbnail"]["source"]

                # print(url)

                item["http://schema.org/image"] = [
                    {
                        "@id": url
                    }
                ]


path = "data/all.json"

with open(path, 'w') as outfile:
    json.dump(items, outfile, ensure_ascii=False,
        indent=4, sort_keys=True, separators=(',', ': '))