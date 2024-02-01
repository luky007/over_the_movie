"""Script for importing the csv files given by "Over the movie" into a mySQL server."""

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import coloredlogs  # type: ignore # pyright: ignore[reportMissingTypeStubs]
import mysql.connector as myc
from csv_utils import read_csv_movie, read_csv_ratings, read_csv_users
from db_connection import drop_all_tables, execute_sql_file, load_db


if TYPE_CHECKING:
    from mysql.connector.abstracts import MySQLConnectionAbstract
    from mysql.connector.pooling import PooledMySQLConnection


def main() -> None:
    """The main function."""
    coloredlogs.install()  # pyright: ignore[reportUnknownMemberType]
    path_current_folder = Path(__file__).resolve().parent
    logger = logging.getLogger(Path(__file__).stem)
    logger.setLevel(logging.INFO)

    list_movies = read_csv_movie(
        path_current_folder.parent / "csv" / "input" / "movies.csv"
    )
    list_users = read_csv_users(
        path_current_folder.parent / "csv" / "input" / "users.csv",
        path_current_folder.parent / "csv" / "input" / "comuni.json",
    )
    list_ratings = read_csv_ratings(
        path_current_folder.parent / "csv" / "input" / "ratings.csv",
    )
    connection: PooledMySQLConnection | MySQLConnectionAbstract = myc.connect(
        host="localhost", user="root", password="root", database="over_the_movie_dev"
    )
    drop_all_tables(connection=connection)
    execute_sql_file(
        connection=connection,
        path_sql=Path(path_current_folder.parent / "sql" / "create_tables").with_suffix(
            ".sql"
        ),
    )
    load_db(
        connection=connection,
        list_movies=list_movies,
        list_users=list_users,
        list_ratings=list_ratings,
    )


if __name__ == "__main__":
    main()
