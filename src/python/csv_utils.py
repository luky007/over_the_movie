"""Utils definitions for reading and writing csv files."""
import csv
import json
import logging
import re
import sys
from pathlib import Path

from movie import Movie, Rating, User


def read_csv_movie(path_csv: Path) -> list[Movie]:  # noqa: PLR0915
    """Read the Movie csv given by "Over the movie". Skip the line if errors.

    Args:
        path_csv (Path): the path of the .csv to read.

    Returns:
        list[Movie]: a list an Movie object.

    Do these checks on the csv:
    - Check if there are exactly 3 columns
    - Check if movie_id is unique
    - check if movie has a number indicating the year of release
    - check if year of release is lower than 2024
    - check if year of release is higher than 1888
    - check if there at least one genre
    - check if there repeated genre in the same movie
    - check if the title exist
    - check if the original title exist
    - check if the title and the original title are the same
    - check if some movies share the same title and year of release
    - Check if movie exist based on title and year of release
    - Fix some known typo in the genre
    - Try to fix the title by removing the last comma
    - Remove 'a.k.a.' from the original title
    - Remove second 'a.k.a.' from movie id: 2952
    """
    logger = logging.getLogger(Path(__file__).stem)
    (
        max_column_allowed,
        max_elem_btw_bracket,
        min_year_release,
        max_year_release,
    ) = 3, 2, 1888, 2024
    with open(path_csv, encoding="UTF-8") as file:
        list_movieid: set[int] = set()
        dict_name_movie_year: dict[str, int] = {}
        list_movies: list[Movie] = []

        csv_reader = csv.DictReader(file, delimiter=",")
        for i, row in enumerate(csv_reader, start=1):
            orig_movie_name = None
            if len(row) > max_column_allowed:
                sys.exit("Expected only 3 columns")
            movie_id_raw, title_raw, genres_raw = (
                row["MovieID"],
                row["Title"],
                row["Genres"],
            )

            try:
                movie_id = int(movie_id_raw)
            except ValueError:
                logger.warning(
                    "SKIPPED: The movie id need to be an int. Now is %s Line %s",
                    movie_id_raw,
                    i,
                )
                continue

            if movie_id in list_movieid:
                sys.exit(f"The movie_id is not unique. Line {i}")
            list_movieid.add(movie_id)

            title_regx = re.findall(r"^(.*?)\(", title_raw)
            if not title_regx:
                logger.warning("SKIPPED: %s Year movie not found. Line %s", row, i)
                continue
            title = str(title_regx[0].strip())

            matches_betw_bracket = re.findall(r"\((.*?)\)", title_raw)
            if len(matches_betw_bracket) == 1:
                year_movie = matches_betw_bracket[0]
            elif len(matches_betw_bracket) == max_elem_btw_bracket:
                orig_movie_name, year_movie = matches_betw_bracket
            else:
                logger.warning(
                    "SKIPPED: %s has too many element between bracket. Line %s",
                    title_raw,
                    i,
                )
                continue
            list_genres_current_row = genres_raw.split("|")

            try:
                year_movie = int(year_movie)
            except ValueError:
                logger.warning(
                    "SKIPPED: Year need to be an int. Now is %s Line %s", year_movie, i
                )
                continue
            if year_movie < min_year_release:
                logger.warning(
                    "SKIPPED: Year must be higher than %s. Now is: %s Line %s",
                    min_year_release,
                    year_movie,
                    i,
                )
                continue
            if year_movie > max_year_release:
                logger.warning(
                    "SKIPPED: Year must be lower than %s. Now is: %s Line %s",
                    max_year_release,
                    year_movie,
                    i,
                )
                continue

            if len(list_genres_current_row) == 0:
                logger.warning(
                    "SKIPPED: %s The genres cannot be empty. Line %s", row, i
                )
                continue
            if len(list_genres_current_row) != len(set(list_genres_current_row)):
                logger.warning(
                    "SKIPPED: %s The genres cannot be repeated. Line %s", row, i
                )
                continue

            if len(title) == 0:
                logger.warning("SKIPPED: %s The title cannot be empty. Line %s", row, i)
                continue
            if orig_movie_name is not None and len(orig_movie_name) == 0:
                logger.warning(
                    "SKIPPED: %s The original title cannot be empty. Line %s", row, i
                )
                continue
            if orig_movie_name is not None and title.strip() == orig_movie_name.strip():
                logger.warning(
                    "SKIPPED: %s The original title and title are equal. Line %s",
                    row,
                    i,
                )
                continue
            if orig_movie_name is not None and orig_movie_name.find("a.k.a. ") != -1:
                if orig_movie_name == "a.k.a. Sydney, a.k.a. Hard Eight":
                    orig_movie_name = "Sydney"
                    logger.info(
                        "CHANGED: %s Remove double aka, now is %s Line %s",
                        row,
                        orig_movie_name,
                        i,
                    )
                else:
                    orig_movie_name = str(orig_movie_name.split("a.k.a. ")[1])
                    logger.info(
                        "CHANGED: %s Remove single aka, now is %s. Line %s",
                        row,
                        orig_movie_name,
                        i,
                    )
            if (
                title in dict_name_movie_year
                and dict_name_movie_year.get(str(year_movie)) == year_movie
            ):
                logger.warning(
                    "SKIPPED: %s Film equal in name and year. Line %s", row, i
                )
                continue
            dict_name_movie_year[str(title)] = year_movie

            title = str(re.sub(r",\s[A-Z]\w*$", "", title))
            orig_movie_name = str(re.sub(r",\s[A-Z]\w*$", "", str(orig_movie_name)))

            list_genres_current_row = fix_genres(
                list_genres_current_row, counter_line=i, raw_line=str(row)
            )

            list_movies.append(
                Movie(
                    movie_id=movie_id,
                    title=title,
                    orig_movie_name=orig_movie_name,
                    year_movie=year_movie,
                    list_genres_current_row=list_genres_current_row,
                )
            )

        return list_movies


def fix_genres(
    list_genres_current_row: list[str], raw_line: str, counter_line: int
) -> list[str]:
    """Fix the errors in the genres.

    Args:
        list_genres_current_row (list[str]): a list containing the genres
        raw_line (list[str]): the raw input line to process
        counter_line (int): the line number of the input. Used for logging only

    Returns:
        list[str]: the fixed list containing the genres
    """
    logger = logging.getLogger(Path(__file__).stem)
    for genres in list_genres_current_row.copy():
        if genres == "Dramatic":
            list_genres_current_row.remove("Dramatic")
            list_genres_current_row.append("Drama")
            logger.info(
                "CHANGED: %s Changed genre from Dramatic to Drama. Line %s",
                raw_line,
                counter_line,
            )
        if genres == "Dramma":
            list_genres_current_row.remove("Dramma")
            list_genres_current_row.append("Drama")
            logger.info(
                "CHANGED: %s Changed genre from Dramma to Drama. Line %s",
                raw_line,
                counter_line,
            )
        if genres == "Comedy--Horror":
            list_genres_current_row.remove("Comedy--Horror")
            list_genres_current_row.append("Horror")
            list_genres_current_row.append("Comedy")
            logger.info(
                "CHANGED: %s Changed genre from Comedy--Horror to Comedy and Horror. Line %s",
                raw_line,
                counter_line,
            )
    return list_genres_current_row


def read_csv_users(path_csv: Path, path_json_cap: Path) -> list[User]:
    """Read the Users csv given by "Over the movie". Skip the line if errors.

    Args:
        path_csv (Path): the path of the .csv to read.
        path_json_cap (Path): the path of .json containing the informations about the CAP.

    Returns:
        list[users]: a list an User object.
    """
    logger = logging.getLogger(Path(__file__).stem)
    max_column_allowed, max_user_age_allowed, min_user_age_allowed = 5, 6, 100
    with open(path_json_cap, encoding="UTF-8") as file:
        list_all_cap = [comune["cap"] for comune in json.load(file)]
        set_all_cap = {item for sublist in list_all_cap for item in sublist}
    list_users: list[User] = []
    with open(path_csv, encoding="UTF-8") as file:
        csv_reader = csv.DictReader(file, delimiter=",")
        list_userid: set[int] = set()
        for i, row in enumerate(csv_reader, start=1):
            if len(row) > max_column_allowed:
                sys.exit(f"Expected only {max_column_allowed} columns")
            user_id, gender, age_raw, cap_raw, job = (
                row["UserID"],
                row["Gender"],
                row["Age"],
                row["CAP"],
                row["Work"],
            )
            try:
                user_id = int(user_id)
            except ValueError:
                logger.warning(
                    "SKIPPED: The movie id need to be an int. Now is %s Line %s",
                    user_id,
                    i,
                )
                continue
            if user_id in list_userid:
                sys.exit(f"The user_id is not unique. Line {i}")
            list_userid.add(user_id)

            if gender not in ["M", "F"]:
                logger.warning("SKIPPED: %s Is not 'M' nor 'F'. Line %s", row, i)
                continue

            try:
                age = int(age_raw)
            except ValueError:
                logger.warning(
                    "SKIPPED: The age need to be an int. Now is %s Line %s",
                    age_raw,
                    i,
                )
                continue

            if (
                age_raw.isdigit()
                and int(age_raw) < min_user_age_allowed
                or int(age_raw) > max_user_age_allowed
            ):
                logger.warning("SKIPPED: %s The yob is not plausible. Line %s", row, i)
                continue

            if cap_raw not in set_all_cap:
                logger.warning("SKIPPED: %s The cap is unknown. Line %s", cap_raw, i)
                continue

            try:
                cap = int(cap_raw)
            except ValueError:
                logger.warning(
                    "SKIPPED: The CAP need to be an int. Now is %s Line %s",
                    age_raw,
                    i,
                )
                continue

            if job == "Data Scientis":
                logger.info(
                    "CHANGED: %s Replaced 'Data scientis' with 'Data scientist'. Line %s",
                    row,
                    i,
                )

            list_users.append(
                User(
                    user_id=user_id,
                    gender="M" if gender == "M" else "F",
                    age=age,
                    cap=cap,
                    job=job,
                )
            )
    return list_users


def read_csv_ratings(path_csv: Path) -> list[Rating]:
    """Read the Ratings csv given by "Over the movie". Skip the line if errors.

    Args:
        path_csv (Path): the path of the .csv to read.

    Returns:
        list[users]: a list an User object.
    """
    logger = logging.getLogger(Path(__file__).stem)
    max_column_allowed, max_allowed_rating = 4, 5
    list_rating: list[Rating] = []
    with open(path_csv, encoding="UTF-8") as file:
        list_userid: set[int] = set()
        list_movieid: set[int] = set()
        csv_reader = csv.DictReader(file, delimiter=",")
        for i, row in enumerate(csv_reader, start=1):
            if len(row) > max_column_allowed:
                sys.exit(f"Expected only {max_column_allowed} columns in ratings csv")
            user_id_raw, movie_id_raw, rating_raw, timestamp_raw = (
                row["UserID"],
                row["MovieID"],
                row["Rating"],
                row["Timestamp"],
            )
            try:
                user_id = int(user_id_raw)
            except ValueError:
                logger.warning(
                    "SKIPPED: The user id need to be an int. Now is %s Line %s",
                    user_id_raw,
                    i,
                )
                continue
            try:
                movie_id = int(movie_id_raw)
            except ValueError:
                logger.warning(
                    "SKIPPED: The movie id need to be an int. Now is %s Line %s",
                    movie_id_raw,
                    i,
                )
                continue
            try:
                rating = int(rating_raw)
            except ValueError:
                logger.warning(
                    "SKIPPED: The rating need to be an int. Now is %s Line %s",
                    rating_raw,
                    i,
                )
                continue
            try:
                timestamp = int(timestamp_raw)
            except ValueError:
                logger.warning(
                    "SKIPPED: The timestamp need to be an int. Now is %s Line %s",
                    timestamp_raw,
                    i,
                )
                continue

            if rating > max_allowed_rating or rating < 1:
                logger.warning(
                    "SKIPPED: The rating in not within 1-%s. Now is %s Line %s",
                    max_allowed_rating,
                    rating,
                    i,
                )
                continue

            list_movieid.add(movie_id)
            list_userid.add(user_id)
            list_rating.append(
                Rating(
                    user_id=user_id,
                    movie_id=movie_id,
                    rating=rating,
                    timestamp=timestamp,
                )
            )
    return list_rating


def write_csv_movie(path_csv: Path, list_movies: list[Movie]) -> None:
    """Write the clean csv movie file.

    Args:
        path_csv (Path): the path of the csv file to write.
        list_movies (list[Movie]): the list of movies to write.
    """
    with open(
        path_csv,
        mode="w",
        encoding="UTF-8",
        newline="",
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["movie_id", "title", "original_title", "year_movie", "genre"])
        for movie in list_movies:
            movie_id = movie.movie_id
            title = movie.title
            orig_movie_name = movie.orig_movie_name
            year_movie = movie.year_movie
            list_genres_current_row = movie.list_genres_current_row
            writer.writerow(
                [
                    movie_id,
                    title,
                    orig_movie_name,
                    year_movie,
                    "|".join(list_genres_current_row),
                ]
            )
