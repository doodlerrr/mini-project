import bp as bp
from flask import Flask, render_template, \
    request, url_for, redirect, flash, session,\
    abort, jsonify,g
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import timedelta, datetime
import jwt
import hashlib

app = Flask(__name__)
app.config["SECRET_KEY"] = "dfsdvasdadfadfafwafrg"
SECRET_KEY = 'SPARTA'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1)
client = MongoClient('mongodb+srv://test:sparta@cluster0.nbw8ry5.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.mini

# 메인
@app.route("/")
def main():
    posts = db.posts
    datas = list(posts.find({}))
    return render_template("main.html", datas=datas)

# 글쓰기
@app.route("/write", methods=["GET","POST"])
def write():
    if session.get('id') is None:
        return redirect("login")

    if request.method == "POST":
        title = request.form.get("title")
        contents = request.form.get("contents")
        tag = request.form.get("tag")
        url = request.form.get("url")

        posts = db.posts
        post = {
            "writer_id": session.get("id"),
            "title": title,
            "contents": contents,
            "tag": tag,
            "url": url,
        }

        inserted_data = posts.insert_one(post)
        return redirect(url_for("main", _id = inserted_data.inserted_id))
    else:
        return render_template("write.html")

# 회원가입
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", type=str)
        email = request.form.get("email", type=str)
        password = request.form.get("password", type=str)
        re_password = request.form.get("re_password", type=str)

        if name == "" or email == "" or password == "" or re_password == "":
            flash("입력되지 않은 값이 있습니다.")
            return render_template('signup.html')

        if password != re_password:
            flash('비밀번호가 일치하지 않습니다.')
            return render_template('signup.html')

        members = db.members
        count = members.count_documents({"email": email})
        print(count)
        if count > 0:
            flash("중복된 이메일 주소입니다.")
            return render_template("signup.html")

        info = {
            "name": name,
            "email": email,
            "password": password,
            "re_password": re_password
        }
        members.insert_one(info)
        flash('성공적으로 가입되었습니다.')
        return render_template("login.html")
    else:
        return render_template("signup.html")

# 글 조회
@app.route("/get/<idx>")
def get(idx):
    if idx is not None:
        posts = db.posts
        data = posts.find_one({"_id": ObjectId(idx)})

        if data is not None:
            post = {
                "id": data.get("_id"),
                "name": data.get("name"),
                "title": data.get("title"),
                "contents": data.get("contents"),
                "url":data.get("url"),
                "writer_id": data.get("writer_id", "")
            }

            return render_template(
                "get_one.html",
                post=post
            )
    return abort(404)

# 수정
@app.route("/amend/<idx>", methods=['GET','POST'])
def amend(idx):
    if request.method == "GET":
        posts = db.posts
        data = posts.find_one({"_id": ObjectId(idx)})
        if data is None:
            flash("해당 게시글이 존재하지 않습니다.")
            redirect(url_for("main"))
        else:
            if session.get("id") == data.get("writer_id"):
                return render_template('amend.html', data=data)
            else:
                flash("글 수정 권한이 없습니다.")
                return redirect(url_for("main"))
    else:
        title = request.form.get('title')
        contents = request.form.get('contents')
        tag = request.form.get('tag')
        url = request.form.get('url')

        posts = db.posts
        data = posts.find_one({"_id": ObjectId(idx)})
        if session.get("id") == data.get("writer_id"):
            posts.update_one({"_id": ObjectId(idx)}, {
                "$set": {
                    "title": title,
                    "contents": contents,
                    "tag": tag,
                    "url": url
                }
            })
            flash("수정되었습니다.")
            return redirect(url_for("get", idx=idx))
        else:
            flash("수정 권한이 없습니다.")
            return redirect(url_for("main"))

# 삭제
# 로그인
@app.route("/login", methods=["GET", "POST"])
def member_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")

        members = db.members
        data = members.find_one({"email": email})

        if data is None:
            flash("회원 정보가 없습니다.")
            return redirect(url_for("member_login"))
        else:
            if data.get("password") == password:
                session["email"] = email
                session["name"] = data.get("name")
                session["id"] = str(data.get("_id"))
                session.permanent = True
                flash(session["name"] + '(님)' + " 로그인 되었습니다.")
                return redirect(url_for("main"))
            else:
                flash("비밀번호가 일치하지 않습니다.")
                return redirect(url_for("member_login"))
        return ''
    else:
        return render_template("login.html")

# 로그아웃
@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect('/')

# # 로그인 최종
# @app.route('/login')
# def login():
#     return render_template('final_login.html')
#
#
# @app.route('/membership')
# def membership():
#     return render_template('membership.html')
#
# @app.route('/membership/login', methods=['POST'])
# def sign_in():
#     # 로그인
#     username_receive = request.form['username_give']
#     password_receive = request.form['password_give']
#
#     pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
#     result = db.membership.find_one({'username': username_receive, 'password': pw_hash})
#
#     if result is not None:
#         payload = {
#             'id': username_receive,
#             'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
#         }
#         token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
#
#         return jsonify({'result': 'success', 'token': token})
#     # 찾지 못하면
#     else:
#         return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
#
# # [아이디 중복검사 API]
# # id 중복검사및 유효성 검사를 합니다.
#
# @app.route('/membership/check_dup', methods=['POST'])
# def check_dup():
#     username_receive = request.form['username_give']
#     exists = bool(db.membership.find_one({"username": username_receive}))
#     return jsonify({'result': 'success', 'exists': exists})
#
#
# # [회원가입 API]
# # id, pw, name을 받아서, mongoDB에 저장합니다.
# # 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
# @app.route('/membership/save', methods=['POST'])
# def sign_up():
#     username_receive = request.form['username_give']
#     password_receive = request.form['password_give']
#     name_receive = request.form['name_give']
#
#     password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
#
#     doc = {
#         "username": username_receive,  # 아이디
#         "password": password_hash,  # 비밀번호
#         "name": name_receive  # 이름
#     }
#     db.membership.insert_one(doc)
#
#     return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)