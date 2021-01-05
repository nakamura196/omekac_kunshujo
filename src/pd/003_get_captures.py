import json


OUTPUT_FILE = "data/captures.json"
captureIds = []

# path to curation
curation_path = "../../docs/curation/test.json"

count = 0

with open(curation_path) as f:
    curation = json.load(f)

    selections = curation["selections"]

    for selection in selections:
        members = selection["members"]

        for member in members:

            captureIds.append(member["@id"])

# Write out data
with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(captureIds, outfile, ensure_ascii=False,
              indent=4, sort_keys=True, separators=(',', ': '))
print("Wrote " + str(len(captureIds)) + " lines to " + OUTPUT_FILE)
