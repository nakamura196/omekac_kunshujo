from PIL import Image, ImageDraw

def show_bbox(image_path):
    # image_pathのフォルダ名と拡張子を変更してラベルファイルのパスを作る
    label_path = image_path.replace('/images/', '/labels/').replace('.jpg', '.txt')

    # 画像を開き、描画ようにImageDrawを作る
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    with open(label_path, 'r') as f:
        for line in f.readlines():
            # 一行ごとに処理する
            label, x, y, w, h = line.split(' ')

            # 文字から数値に変換
            x = float(x)
            y = float(y)
            w = float(w)
            h = float(h)

            # 中央位置と幅と高さ => 左上、右下位置
            W, H = image.size
            x1 = (x - w/2) * W
            y1 = (y - h/2) * H
            x2 = (x + w/2) * W
            y2 = (y + h/2) * H

            # BoundingBoxを赤線で囲む
            draw.rectangle((x1, y1, x2, y2), outline=(255, 0, 0), width=5)

    image.show()

name = "0d2b830723cbd92721c1e278dec47ada.jpg"    

show_bbox('/Users/nakamurasatoru/git/d_omeka/omekac_kunshujo/docs/files/yolov5_416x416-black-padding.v2/train/images/' + name)
# show_bbox('/Users/nakamurasatoru/Downloads/aaaab/valid/images/shutterstock_1145933543-e1579497052960_jpg.rf.f3807b96202c59d946e24047e52e92d0.jpg')