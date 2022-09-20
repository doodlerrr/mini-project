from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

import certifi
ca = certifi.where()

client = MongoClient('#', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

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
    app.run('0.0.0.0', port=5000, debug=True)
