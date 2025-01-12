#-----------------------------------------------------------------------#
#   predict.py将单张图片预测、摄像头检测、FPS测试和目录遍历检测等功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
#-----------------------------------------------------------------------#
import time
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from PIL import Image
import cv2
import numpy as np
from PIL import Image

from ljh import YOLO
import random
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
def process_image(image_path):
    # 定义图片的保存路径
    yolo = YOLO()
    save_path = "static/"

    # 生成一个随机文件名
    random_filename = f"{random.randint(100000, 999999)}.jpg"

    # 指定完整的保存路径和文件名
    full_save_path = os.path.join(save_path, random_filename)
    save_path = full_save_path  # 指定保存图片的路径
    a = 1
    while a:
        img = image_path
        try:
            image = Image.open(img)
            print('11')
        except:
            print('Open Error! Try again!')
            continue
        else:
            lab,bestscore,r_image,cla = yolo.detect_image(image, crop=False, count=False)
            r_image.save(save_path)  # 保存图片
            a = 0
            print('b',bestscore)
            if lab != 0:
                return {
                    "flag":1,
                    "class": cla,
                    "score":float(bestscore),
                    "picture": save_path
                }
            else:
                return {
                    "flag":0,
                    "score":75,
                    "picture": save_path
                }


@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    if request.method == 'OPTIONS':
        # 返回CORS头部，允许来自指定来源的请求
        response = jsonify({})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    # 正常处理上传请求
    file = request.files['file']
    filename = secure_filename(file.filename)
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    file_path = os.path.join('tmp', filename)
    file.save(file_path)

    try:
        print('file_path', file_path)
        result = process_image(file_path)
        result['picture'] = request.host_url + 'static/' + result['picture'].split('/')[-1]
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    return jsonify(result), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

