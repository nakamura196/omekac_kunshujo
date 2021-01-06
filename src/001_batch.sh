# メタデータ取得
# python 201_CollectionGenerator.py
# python 202_ManifestGenerator.py
echo "python 203_CreateCuration.py"
python 203_CreateCuration.py
# python 250_GetAnnos.py

# 類似画像検索
python 010_download_thumbnail.py
python 120_process_images.py
# python 130_build.py
# python 140_predict.py
python 150_updateCuration.py

# 類似テキスト
python 520_textSim.py

# 事物
python 301_createHand.py
python 302_createApi.py
python 304_updateCuration.py

# yolo
python 400_download_larges.py

cd yolo
source myenv/bin/activate
python pred.py
deactivate
cd ../
python 401_addTags.py