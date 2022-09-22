from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.iuqpqy6.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta

# 하다가 잘 안된.. 수정 페이지입니다.

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/amend", methods=["GET"])
def test_get():
    contents = list(db.contents.find({},{'_id':False}))
    return jsonify({'contents': contents})

    user = db.users.find_one({'name': 'bobby'})
    print(db.contents.find({}))
@app.route('/amend', methods=['POST'])
def test_post():
    title = request.form['title']
    main = request.form['main']
    tag = request.form['tag']
    url = request.form['url']

    db.contents.update_one({'title': title}, {'$set': {'title' : title, 'main': main, 'tag': tag, 'url': url}})

    # doc = {
    #     'title': title,
    #     'main': main,
    #     'tag': tag,
    #     'url': url
    # }
    #
    # db.contents.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '수정 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)