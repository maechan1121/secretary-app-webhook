
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    return 'Hello World!'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers['Content-Type'] != 'application/json':
        print('type:'+request.headers['Content-Type'])
        return 'type:'

    print ("ok")

    return jsonify(res='ok')

if __name__ == '__main__':
    app.run()

