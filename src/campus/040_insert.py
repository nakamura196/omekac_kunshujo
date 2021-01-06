import gspread
import json

#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 

#############

col_size = 14

#############

main_path = "data/tags.json"

with open(main_path) as f:
    tags = json.load(f)

tags_sorted = sorted(tags.items(), key=lambda x:x[1], reverse=True)

tags_sorted = tags_sorted[0:2000]

print(len(tags_sorted))

row_size = len(tags_sorted) + 10000

#############

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('quickstart-1582120675559-d3d5f165fdc8.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1RyPtvYi5hLTjPXZRO8gTeS9F32vy8RYYbVz-UI1-jy0'

worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

ds = worksheet.range("A1:N"+str(row_size))

exist_values = {}

structured = {}

for i in range(1, row_size):
    index = i * col_size
    value = ds[index].value

    if value != "":

        exist_values[value] = index

        last_index = index + col_size

        for j in range(0, 6):
            uri = ds[index + 2 + 2 * j].value
            wiki =  ds[index + 3 + 2 * j].value

            if ":" in uri:
                structured[value] = {
                    "uri" : uri
                }
                if wiki != "":
                    structured[value]["wiki"] = wiki
            

start = 0

# '=HYPERLINK("seyepapeseny@gmail.com","email")'

for i in range(1, len(tags_sorted)):
    value = tags_sorted[i][0]
    count = tags_sorted[i][1]

    url = "https://diyhistory.org/public/kunshujo/admin/items/browse?search=&advanced[0][joiner]=and&advanced[0][element_id]=&advanced[0][type]=&advanced[0][terms]=&range=&collection=&type=1&user=&tags="+value+"&public=&featured=&submembers=0&submembers=1&submit_search=アイテムを検索する"

    if value not in exist_values:
        ds[start * col_size + last_index].value = '=HYPERLINK("'+url+'","'+value+'")'
        ds[start * col_size + 1 + last_index].value = count

        start += 1

    else:
        index = exist_values[value]
        
        ds[index].value = '=HYPERLINK("'+url+'","'+value+'")'
        ds[index + 1].value = count

# worksheet.update_cells(ds,value_input_option='USER_ENTERED')

with open("data/structured.json", 'w') as outfile:
    json.dump(structured, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))