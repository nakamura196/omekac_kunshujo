python 001_make_dump.py
python 002_download_images.py
python 003_get_captures.py
python 004_get_metadata.py
python 005_get_color_data.py
python 006_get_colors.py

python 007_stitch_images.py ../data/ /Users/nakamura/git/thumbnail/umesao/ ../../docs/img/ 50 20 20 default 100 10 3 30000
python 007_stitch_images.py ../data/ /Users/nakamura/git/thumbnail/umesao/ ../../docs/img/ 50 20 20 colors 100 10 3 30000
python 007_stitch_images.py ../data/ /Users/nakamura/git/thumbnail/umesao/ ../../docs/img/ 50 20 20 資料種別 100 10 3 30000


python 008_generate_metadata.py
python 009_generate_labels.py ../data/ ../../docs/js/labels.json 100 10 50 20 3
python 010_generate_coordinates.py ../data/ ../../docs/js/coords.json 100 10 10 50 20 3