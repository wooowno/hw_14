from flask import Flask, jsonify, request

from utils import *


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/movie/<title>")
def movie_page(title):
    return jsonify(get_movie_by_title(title))


@app.route("/movie")
def movie_by_year_page():
    _from = request.values.get('from')
    _to = request.values.get('to')
    return jsonify(get_movies_by_year(_from, _to))


@app.route("/rating/children")
def children_movies_page():
    return jsonify(get_movies_by_rating(['G']))


@app.route("/rating/family")
def family_movies_page():
    return jsonify(get_movies_by_rating(['G', 'PG', 'PG-13']))


@app.route("/rating/adult")
def adult_movies_page():
    return jsonify(get_movies_by_rating(['R', 'NC-17']))


@app.route("/genre/<genre>")
def genre_movies_page(genre):
    return jsonify(get_movies_by_genre(genre))


if __name__ == "__main__":
    app.run()
