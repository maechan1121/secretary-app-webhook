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

# row 行, col 列
# google home
def rec(data, gc):
    flg = True

    # 共有設定したスプレッドシートの名前を指定する
    workbook = gc.open("secretary-pointinfo")
    
    worksheet = workbook.worksheet("リスト")

    #以下、動作テスト
    # userID
    uID = data.get("originalDetectIntentRequest").get("payload").get("user").get("userId")

    # 接続機器の登録を確認
    targetcell = cell_search(sheet = worksheet, str = uID)

    if targetcell is not None:
        sheetname = worksheet.cell(targetcell.row, 3).value
        print ("sheetname")
        print (sheetname)

        if sheetname != "":
            worksheet = workbook.worksheet(sheetname)
            
            offset = worksheet.cell(1, 1).value
            print ("offset")
            print (offset)

            if offset == "":
                worksheet.update_cell(1, 1, 0)
                offset = "0"
            else:
                if int(offset) >= 0:
                    flg = True
                else:
                    flg = False
            if flg == True:
                worksheet.update_cell(int(offset) + 2, 1, data.get("queryResult").get("queryText"))
                # 機器登録あり
                data = {"fulfillmentText":' '}
                r = json.dumps(data, indent=4)
                r = make_response(r)
                r.headers['Content-Type'] = 'application/json'
                worksheet.update_cell(1, 1, int(offset) + 1)
                return r
        else :
            flg = False
    else:
        flg = False
        
    if flg == False:
        # 機器登録なし
        data = {"fulfillmentText":'登録されていない機器です'}
        r = json.dumps(data, indent=4)
        r = make_response(r)
        r.headers['Content-Type'] = 'application/json'
        return r





def phoneapp(data, gc):
    r = {"result":"NG"}

    if data.get("types") == "login":
        print (data.get("types"))
        worksheet = gc.open("secretary-pointinfo").worksheet("ログイン")

        cell = cell_search(sheet=worksheet, str=data.get("data").get("userID"))
        print(cell)
        if cell is not None:
            print("1")
            if cell.col == 1:
                print("2")
                print(worksheet.cell(cell.row, 2).value)
                print(data.get("data").get("password"))
                if worksheet.cell(cell.row, 2).value == data.get("data").get("password"):
                    print (format("{0}がログイン", data.get("data").get("userID")))
                    r = {"result":"OK"}
    elif data.get("type") == "getlist":
        worksheet = gc.open("secretary-pointinfo").worksheet("ログイン")
        rows = cell_search(sheet=worksheet, str=data.get("data").get("userID")).row
        itemnum = worksheet.cell(rows, 3).value
        r = {"num" : itemnum}

        items = worksheet.range(cell(rows, 4), cell(rows, 4 + itemnum))

        r['items'] = items


    r = json.dumps(r, indent=4)
    r = make_response(r)
    r.headers['Content-Type'] = 'application/json'
    return r

def cell_search(sheet, str):
    try:
        cell = sheet.find(str)
        
        return cell

    except gspread.exceptions.CellNotFound:
        
        return None

if __name__ == '__main__':
    app.run()

