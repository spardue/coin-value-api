from flask import Flask, request

import coinvalue

app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_value():
    args = request.get_json()
    return coinvalue.get_value(args)