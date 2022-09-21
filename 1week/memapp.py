from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.sojhuso.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

import hashlib


@app.route('/')
def home():
        return render_template('membershtp.html')

# [아이디 중복검사 API]
# id 중복검사및 유효성 검사를 합니다.

@app.route('/membership/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.membership.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

# [회원가입 API]
# id, pw, name을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.

@app.route('/membership/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    name_receive = request.form['name_give']

    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,     # 비밀번호
        "name": name_receive          # 이름
    }
    db.membership.insert_one(doc)

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
