!!! note

    This project is part of a dummy simulation.

## What it does:
- Clean the three input CSV file given by the client.

- Import these inside a mySQL database.

## Complete list of things that it does to the CSV:

### movies.csv
- Check if there are exactly 3 columns
- Check if movie id is unique and a int
- Check if movie has a number indicating the year of release
- Check if year of release is lower than 2024
- Check if year of release is higher than 1888
- Check if there at least one genre
- Check if there repeated genre in the same movie
- Check if the title exist
- Check if the original title exist
- Check if the title and the original title are the same
- Check if some movies share the same title and year of release
- Check if movie exist based on title and year of release
- Fix some known typo in the genre
- Try to fix the title by removing the last comma
- Remove 'a.k.a.' from the original title
- Remove second 'a.k.a.' from movie id: 2952

#### Es. input movies.csv
| MovieID | Title                                                | Genres                         |
|---------|------------------------------------------------------|--------------------------------|
| 1       | Toy Story (1995)                                     | Animation\|Children's\|Comedy  |
| 2       | Jumanji (1995)                                       | Adventure\|Children's\|Fantasy |
| 3       | Grumpier Old Men (1995)                              | Comedy\|Romance                |
| 30      | Shanghai Triad (Yao a yao yao dao waipo qiao) (1995) | Drama                          |

### ratings.csv
- Check if there are exactly 4 columns
- Check if the movie id is unique and a int
- Check if the user id is unique and a int
- Check if the gender is either "M" or "F"
- Check if the user age is a int and within a plausible range
- Check if the postal code (CAP) exists in Italy and is a int
- Fix typo in the job name, "Data scientis" -> "Data scientist"

#### Es. input ratings.csv
| UserID | MovieID | Rating | Timestamp |
|--------|---------|--------|-----------|
| 1      | 1193    | 5      | 978300760 |
| 1      | 661     | 3      | 978302109 |
| 1      | 914     | 3      | 978301968 |
| 2      | 1210    | 4      | 978298151 |

### users.csv
- Check if there are exactly 4 columns
- Check if the movie id is unique and a int
- Check if the user id is unique and a int
- Check if the rating is a int within 1 and 5
- Check if timestamp is a number

#### Es. input users.csv
| UserID | Gender | Age | CAP   | Word          |
|--------|--------|-----|-------|---------------|
| 3      | M      | 24  | 36100 | Autista       |
| 4      | M      | 37  | 85024 | Data Engineer |
| 5      | M      | 15  | 01010 | Studente      |


## Who worked at this:

<style>
    .invert {
        filter: invert(1) hue-rotate(180deg) contrast(1);
    }
</style>
![use_case_diagram](team.excalidraw.png){ .invert }