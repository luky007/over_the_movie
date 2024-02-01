"""Utils definitions for inserting the data into the mysql database."""
from pathlib import Path

from movie import Movie, Rating, User
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

from tqdm import tqdm


def drop_all_tables(
    connection: PooledMySQLConnection | MySQLConnectionAbstract,
) -> None:
    """Drop all the tables created previously.

    Args:
        connection (PooledMySQLConnection | MySQLConnectionAbstract): the connection to use.
    """
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS movies_genres_link;")
        cursor.execute("DROP TABLE IF EXISTS genres;")
        cursor.execute("DROP TABLE IF EXISTS ratings;")
        cursor.execute("DROP TABLE IF EXISTS movies;")
        cursor.execute("DROP TABLE IF EXISTS jobs;")
        cursor.execute("DROP TABLE IF EXISTS users;")
        connection.commit()


def execute_sql_file(
    connection: PooledMySQLConnection | MySQLConnectionAbstract, path_sql: Path
) -> None:
    """Read and execute the sql query within an input file.

    Args:
        connection (PooledMySQLConnection | MySQLConnectionAbstract): the connection to use.
        path_sql (Path): the path of the file .sql to read and execute
    """
    with open(path_sql, encoding="UTF-8") as f:
        sql_create_tables = f.read()
    with connection.cursor() as cursor:
        for sql_command in sql_create_tables.split(";"):
            if sql_command.strip():
                cursor.execute(sql_command.strip(), multi=True)
        connection.commit()


def load_db(
    connection: PooledMySQLConnection | MySQLConnectionAbstract,
    list_movies: list[Movie],
    list_users: list[User],
    list_ratings: list[Rating],
) -> None:
    """Load the data into the database.

    Args:
        connection (PooledMySQLConnection | MySQLConnectionAbstract): the connection to use.
        list_movies (list[Movie]): a list an Movie object.
        list_users (list[User]): a list an User object.
        list_ratings (list[Rating]): a list an Rating object.
    """
    with connection.cursor() as cursor:
        for movie in list_movies:
            cursor.execute(
                "INSERT INTO movies (movie_id, movie_title, movie_original_title, year_release) \
                VALUES (%s,%s,%s,%s)",
                (movie.movie_id, movie.title, movie.orig_movie_name, movie.year_movie),
            )
        connection.commit()

    list_genres: list[str] = []
    for movie in list_movies:
        for genre in movie.list_genres_current_row:
            if genre not in list_genres:
                list_genres.append(genre)

    with connection.cursor() as cursor:
        for i, genre in enumerate(list_genres):
            cursor.execute(
                "INSERT INTO genres (genre_id, genre) VALUES (%s, %s)",
                (i, genre),
            )
        connection.commit()

    dict_movies_genres: dict[int, list[int]] = {}
    for movie in list_movies:
        for genre in movie.list_genres_current_row:
            for i, genre_ref in enumerate(list_genres):
                if genre == genre_ref:
                    if movie.movie_id in dict_movies_genres:
                        dict_movies_genres[movie.movie_id].append(i)
                    else:
                        dict_movies_genres[movie.movie_id] = [i]

    with connection.cursor() as cursor:
        for movie_id, list_genre_id in dict_movies_genres.items():
            for genre_id in list_genre_id:
                cursor.execute(
                    "INSERT INTO movies_genres_link (movie_id, genre_id) VALUES (%s, %s)",
                    (movie_id, genre_id),
                )
        connection.commit()

    list_jobs: list[str] = []
    for user in list_users:
        if user.job not in list_jobs:
            list_jobs.append(user.job)

    with connection.cursor() as cursor:
        for user in list_users:
            cursor.execute(
                "INSERT INTO users (user_id, gender, age, cap, job_id) VALUES (%s,%s,%s,%s,%s)",
                (
                    user.user_id,
                    user.gender,
                    user.age,
                    user.cap,
                    list_jobs.index(user.job),
                ),
            )
        connection.commit()

    with connection.cursor() as cursor:
        for i, job in enumerate(list_jobs):
            cursor.execute(
                "INSERT INTO jobs (job_id, job_type) VALUES (%s, %s)",
                (i, job),
            )
        connection.commit()

    list_movies_id: set[int] = {movie.movie_id for movie in list_movies}
    with connection.cursor() as cursor:
        for rating in tqdm(list_ratings):
            if rating.movie_id not in list_movies_id:
                continue
            cursor.execute(
                "INSERT INTO ratings (user_id,movie_id,rating,timestamp_unix) VALUES (%s,%s,%s,%s)",
                (rating.user_id, rating.movie_id, rating.rating, rating.timestamp),
            )
        connection.commit()
