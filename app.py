from pymongo import MongoClient
from flask import Flask, render_template,request,jsonify
import jwt
import datetime
import hashlib
from datetime import datetime, timedelta
app = Flask(__name__)


client = MongoClient('mongodb://13.209.85.117', 27017, username="test", password="test")
db = client.sparta.sparta.dbsparta.users

SECRET_KEY = 'SPARTA'

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/Membership')
def Membership():
    return render_template("Membership.html")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



   # 로그인
@app.route('/login', methods=['POST'])
def login():

    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
