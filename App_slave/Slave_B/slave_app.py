from flask import Flask, render_template, redirect, request
from Indexer.indexer import Indexer
from DataManager.datamanager import read_doc
import json

app = Flask(__name__)
indexer = Indexer()
app.config['SECRET_KEY'] = '5791628bb0b13ce1c676dfde280ba245'


@app.route('/post_query/<string:query>', methods=['POST', 'GET'])
def post_query(query):
    exp, res = indexer.search(query=query)
    print(res)
    res = list(map(lambda x: {'article_path': 'view_doc/' + x, 'article_content': read_doc(x)[:1000]}, res))
    return render_template('search_resuts.html', posts=res[:10], exp=exp)


@app.route('/add_document', methods=['POST'])
def add_document():
    doc = request.data.decode('ascii')
    doc = doc.split('\n')
    path = doc[0]
    doc = "\n".join(doc[1:])
    print("Received document with path: ", path)
    indexer((path, doc))
    return "Success"


@app.route('/view_doc/.misc/docs/<string:folder>/<string:file>', methods=['GET', 'POST'])
def view_doc(folder, file):
    return read_doc(f'.misc/docs/{folder}/{file}')


@app.route('/', methods=['GET'])
def default():
    return "<H1>Welcome to slave number B</H1>"


if __name__ == '__main__':
    app.run(debug=True, port=6500)
