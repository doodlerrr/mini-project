from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

import certifi
ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.iuqpqy6.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/test', methods=['GET'])
# def test_get():
#    title_receive = request.args.get('title_give')
#    print(title_receive)
#    return jsonify({'result': 'success', 'msg': '이 요청은 GET!'})

@app.route('/registration', methods=['POST'])
def test_post():
    title = request.form['title']
    main = request.form['main']
    tag = request.form['tag']
    url = request.form['url']

    doc = {
        'title' : title,
        'main' : main,
        'tag' : tag,
        'url' : url
    }

    db.contents.insert_one(doc)

    return jsonify({'result':'success', 'msg': 'DB 저장!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)