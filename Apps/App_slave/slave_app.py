import base64
from io import BytesIO

from flask import Flask, render_template, request, send_from_directory, send_file
from System.Indexer.indexer import Indexer
from System.DataManager.datamanager import read_doc

app = Flask(__name__)
indexer = Indexer()
app.config['SECRET_KEY'] = '5791628bb0b13ce1c676dfde280ba245'


@app.route('/post_query/<string:query>', methods=['POST', 'GET'])
def post_query(query):
    exp = 'Not found'
    try:
        exp, res = indexer.search(query=query)
        print(indexer.search(query=query))
        res = list(map(lambda x: {'article_path': 'view_doc/' + x, 'article_content': read_doc(x)[:1000]}, res))
    except:
        res = []
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


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/view_doc/.misc/docs/<string:folder>/<string:file>', methods=['GET', 'POST'])
def view_doc(folder, file):
    return read_doc(f'.misc/docs/{folder}/{file}')


@app.route('/get_pic/<string:index>', methods=['GET', 'POST'])
def get_pic(index):
    x = 'Failed'
    print("../" + index)
    return send_file(index, mimetype='image/png', as_attachment=True, cache_timeout=0)


@app.route('/post_doc/<string:doc_id>', methods=['GET'])
def post_doc(doc_id):
    pass



@app.route('/', methods=['GET'])
def default():
    try:
        variance = indexer.pca_visualize()
    except:
        return render_template('visualize.html')
        print("Couldnt render")
    print(variance)
    return render_template('visualize.html', title='Visualization Textual results', variance=variance)


if __name__ == '__main__':
    try:
        app.run(debug=True, port=5500)
    except:
        app.run(debug=True, port=6500)
