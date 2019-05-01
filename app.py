# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

#google spreadsheetの使用
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#.envの使用
import os

#json
import json

#ここからflaskでcorsの設定 ajaxを使う時のクロスドメイン制約用
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)       #クロスドメイン制約回避のおまじない

@app.route('/', methods=['POST', 'GET'])
def home():
    return 'Hello World!'


@app.route('/webhook', methods=['POST'])
def webhook():
    
    data = request.get_json(force=True, silent=True)

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
    gc = gspread.authorize(credentials)
    
    result = data.get('queryResult')
    if result is not None:
        r = rec(data = data, gc = gc)
        print (json.dumps(data, indent=4))
    else:
        print("Other Access")
        r = phoneapp(data = data, gc = gc)
    return r

def rec(data, gc):
    # 共有設定したスプレッドシートの名前を指定する
    worksheet = gc.open("secretary-pointinfo").worksheet("リスト")
    
    #以下、動作テスト
    # 登録機器数を取得
    devNum = worksheet.cell(1,2).value

    #機器名リスト
    devList = worksheet.col_values(1)

    # userID
    uID = data.get("originalDetectIntentRequest").get("payload").get("user").get("userId")
    try:
        celll = worksheet.find("aaaa")
        print ("a")

    except gspread.exceptions.CellNotFound:
        print ("B")

    print ("usetID:")
    print (uID)

    parameters = data.get('queryResult').get('parameters')
    strs = parameters.get('any')

    print ("devnum:")
    print (devNum)
    print ("devlist:")
    print (devList)

    

    #r = make_response(jsonify(speach='OK',displayText='OK'))
    data = {"fulfillmentText":' '}
    r = json.dumps(data, indent=4)
    r = make_response(r)
    r.headers['Content-Type'] = 'application/json'

    print (r)

    print(strs)

    return r

def phoneapp(data, gc):
#     workbook = worksheet = gc.open("secretary-pointinfo")
#     workbook.add_worksheet(title="testq", rows=100, cols=20)
    r = {"test":"ok"}
    r = json.dumps(r, indent=4)
    r = make_response(r)
    r.headers['Content-Type'] = 'application/json'
    print (r)
    
    return r

if __name__ == '__main__':
    app.run()

