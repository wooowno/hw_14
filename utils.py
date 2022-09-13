import sqlite3
import  json


def load_date(sqlite_query: str) -> list[tuple]:
    """ Возвращает запрашиваемое из базы данных """

    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        cursor.execute(sqlite_query)
        return cursor.fetchall()


def make_list_dict_format(keys: list, data: list[tuple]) -> list[dict]:
    """ Приводит данные к формату list[dict] """

    movies = []

    for movie_data in data:
        movie = {}

        for i in range(len(keys)):
            movie[keys[i]] = movie_data[i]

        movies.append(movie)

    return movies


def get_movie_by_title(title: str) -> list[dict]:
    """ Возвращает фильм с соответствующим названием """

    query = f"""
            SELECT title, country, release_year, listed_in, description
            FROM netflix
            WHERE title = '{title}'
            ORDER BY release_year DESC
            LIMIT 1
            """

    keys = ['title', 'country', 'release_year', 'genre', 'description']
    movie = make_list_dict_format(keys, load_date(query))

    return movie


def get_movies_by_year(_from: int, _to: int) -> list[dict]:
    """ Возвращает список фильмов вышедших в заданный промежуток лет """

    query = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {_from} AND {_to}
            LIMIT 100
            """

    keys = ['title', 'release_year']
    movies = make_list_dict_format(keys, load_date(query))

    return movies


def get_movies_by_rating(rating: list) -> list[dict]:
    """ Возвращает список фильмов с соответствующим рейтингом """

    query = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating IN ('{"', '".join(rating)}')
            """

    keys = ['title', 'rating', 'description']
    movies = make_list_dict_format(keys, load_date(query))

    return movies


def get_movies_by_genre(genre: str) -> list[dict]:
    """ Возвращает список фильмов по жанру """

    query = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            """

    keys = ['title', 'description']
    movies = make_list_dict_format(keys, load_date(query))

    return movies


def get_movies_by_actors(actor_1, actor_2):
    """ Возвращает список тех, кто играет с ними в паре больше 2 раз  """

    query = f"""
            SELECT "cast"
            FROM netflix
            WHERE "cast" LIKE '%{actor_1}%'
            AND "cast" LIKE '%{actor_2}%'
            """
    cast = []

    for line in load_date(query):
        line = set(line[0].split(', '))
        cast.append(line)

    actors_list = set()

    for i in range(2, len(cast)):
        intersection = cast[i-2].intersection(cast[i-1]).intersection(cast[i])
        actors_list.update(intersection)

    actors_list = actors_list.difference({actor_1, actor_2})

    return list(actors_list)


def get_movies_by_type_year_genre(_type: str, release_year: int, genre: str):
    """ Возвращает список фильмов в json по типу, году выхода и жанру """

    query = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            AND type = '{_type}'
            AND release_year = {release_year}
            """

    keys = ['title', 'description']
    return json.dumps(make_list_dict_format(keys, load_date(query)))
