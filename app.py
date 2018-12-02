# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

#google spreadsheetの使用
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#.envの使用
import os

#マルチスレッド
import threading

#ここからflaskでcorsの設定 ajaxを使う時のクロスドメイン制約用
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)       #クロスドメイン制約回避のおまじない

@app.route('/', methods=['POST', 'GET'])
def home():
    return 'Hello World!'

@app.route('/webhook', methods=['POST'])
def webhook():

    print('1')
    
    data = request.get_json(force=True, silent=True)

    thread1 = threading.Thread(target=func(mes=data))

    thread1.start()

    print (data)
    
    return jsonify(res='ok',com='ok')

if __name__ == '__main__':
    app.run()


def func(mes):
    #以下、spreadsheetの操作
    scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

    credential = {
                "type": "service_account",
                "project_id": os.environ['SHEET_PROJECT_ID'],
                "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
                "private_key": os.environ['SHEET_PRYVATE_KEY'],
                "client_email": os.environ['SHEET_CRIENT_EMAIL'],
                "client_id": os.environ['SHEET_CRIENT_ID'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": os.environ['SHEET_CLIENT_X509_CERT_URL']
    }

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential,scope)
    #credentials = ServiceAccountCredentials.from_json_keyfile_name('secretary-api-1e3be6d434e0.json', scope)
    gc = gspread.authorize(credentials)
    # 共有設定したスプレッドシートの名前を指定する
    worksheet = gc.open("secretary-pointinfo").sheet1
    #以下、動作テスト
    # A1セルの値を取得
    print(worksheet.cell(1,1))
    # A1セルを更新
    worksheet.update_cell(1,1, u'Hello, gspread.')

