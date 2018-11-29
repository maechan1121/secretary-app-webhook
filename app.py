
from flask import Flask
from flask import jsonify
from flask import request

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

    print (data)

    return jsonify(res='ok',com='ok')

if __name__ == '__main__':
    app.run()

