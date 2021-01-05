import json

# path to curation
curation_path = "../../docs/curation/test.json"
odir = "data"

count = 0

map = {}

with open(curation_path) as f:
    curation = json.load(f)

    selections = curation["selections"]

    for selection in selections:
        members = selection["members"]

        for member in members:

            metadata = member["metadata"]

            for obj in metadata:
                label = obj["label"]
                value = obj["value"]

                if label not in map:
                    map[label] = {}

                if value not in map[label]:
                    map[label][value] = []
                
                map[label][value].append(count)

            count += 1


for label in map:

    tmp = {}

    result = []
    items_result = []

    obj = map[label]

    count = 0

    for value in obj:
        result.append({
            "count" : len(obj[value]),
            "index" : count,
            "label" : value,
            "url" : "",
            "value" : value
        })

        for index in obj[value]:
            tmp[index] = count

        count += 1

    for index in sorted(tmp):
        items_result.append(tmp[index])

    OUTPUT_FILE = odir + "/"+label+".json"
    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(result, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
    
    OUTPUT_ITEMS_FILE = odir + "/item_"+label+".json"
    with open(OUTPUT_ITEMS_FILE, 'w') as outfile:
        json.dump(items_result, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
