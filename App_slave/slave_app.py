from flask import Flask, render_template, redirect, request
from Indexer.indexer import Indexer
import json

app = Flask(__name__)
indexer = Indexer()
app.config['SECRET_KEY'] = '5791628bb0b13ce1c676dfde280ba245'
"""
import json
s = "{'muffin' : 'lolz', 'foo' : 'kitty'}"
json_acceptable_string = s.replace("'", "\"")
d = json.loads(json_acceptable_string)
"""



@app.route('/post_query', methods=['POST', 'GET'])
def post_query():
    query = request.query_string
    query = 'hi'
    res = indexer.search(query=query)
    print(res)
    return str(" ".join(res))


@app.route('/add_document',methods=['POST'])
def add_document():
    doc = request.data.decode('ascii')
    print(doc)

if __name__ == '__main__':
    app.run(debug=True, port=23569)
