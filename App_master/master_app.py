from flask import Flask, render_template, redirect, request
from html import *
from App_master.forms import SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce1c676dfde280ba245'


@app.route('/')
def landing():
    return redirect('/search', code=302)


@app.route('/search', methods=['GET'])
def search():
    form = SearchForm()
    return render_template('search.html', title='Search',
                           form=form)  # dont forget to add templates folder to 'templates' in project structure


@app.route('/search', methods=['POST'])
def get_results():
    result = request.json
    query = str(request.get_data().split(b'&')[1])[8:-1]

    return render_template('search.html', title='Search', posts=[{'content': 'Article 1 true false'}])


if __name__ == '__main__':
    app.run(debug=True)
