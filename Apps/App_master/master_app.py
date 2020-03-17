from flask import Flask, render_template, redirect, request
from html import *
from Apps.App_master.forms import SearchForm, DocQuery
from load_balancer import LoadBalancer

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce1c676dfde280ba245'
load_balancer = LoadBalancer()





@app.route('/')
def landing():
    return redirect('/search', code=302)


@app.route('/search', methods=['GET'])
def search():
    forms = [SearchForm(), DocQuery()]
    return render_template('search.html', title='Search',
                           forms=forms,
                           slaves=load_balancer.slave_names)  # dont forget to add templates folder to 'templates' in project structure


@app.route('/search', methods=['POST'])
def get_results():
    result = request.json
    print(request.get_data())
    query = str(request.get_data().split(b'&')[1])[8:-1]
    kind = str(request.get_data().split(b'&')[2])[-4:-1]
    posty = 'post_query/'
    if kind == 'Doc':
        posty = 'post_doc/'
        query = query.replace('%2F', '$')

    print(query)

    API_ENDPOINT = load_balancer.get_free_slave()

    data = query
    # sending post request and saving response as response object
    print(API_ENDPOINT + f"/{query}")
    return redirect(API_ENDPOINT + posty + f"{query}", 308)


@app.route('/visualize/<string:slave>', methods=['GET', 'POST'])
def visualize_slave(slave: str):
    slave = load_balancer.get_slave(slave)
    print(slave)

    return redirect(slave, 308)


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


if __name__ == '__main__':
    app.run(debug=True)
