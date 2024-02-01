-- Used as proof of concept for testing the layout of the DB 

DROP DATABASE IF EXISTS over_the_movie_demo;
CREATE DATABASE over_the_movie_demo;
USE over_the_movie_demo;

CREATE TABLE movies (
  film_id INT PRIMARY KEY,
  movie_title VARCHAR(255),
  year_release INT
);
CREATE INDEX idx_movie_title ON movies (movie_title);

CREATE TABLE generi (
  genere_id INT PRIMARY KEY,
  genere VARCHAR(50)
);

CREATE TABLE movie_generi (
  film_id INT,
  genere_id INT,
  FOREIGN KEY (film_id) REFERENCES movies (film_id),
  FOREIGN KEY (genere_id) REFERENCES generi (genere_id)
);

INSERT INTO movies (film_id, movie_title, year_release) VALUES
(1,'Toy Story', 1995),
(2,'Titanic', 1999);

INSERT INTO generi (genere_id, genere) VALUES
(1, "bambini"),
(2, "comico"),
(3, "drammatico");

INSERT INTO movie_generi (film_id, genere_id) VALUES
(1, 1),
(1, 2),
(2, 3);

SELECT * FROM movies;
SELECT * FROM movie_generi;
SELECT * FROM generi;

SELECT m.movie_title, m.year_release, g.genere
FROM movies m
JOIN movie_generi mg ON m.film_id = mg.film_id
JOIN generi g ON mg.genere_id = g.genere_id;

SELECT m.movie_title, m.year_release, GROUP_CONCAT(g.genere) AS genres
FROM movies m
JOIN movie_generi mg ON m.film_id = mg.film_id
JOIN generi g ON mg.genere_id = g.genere_id
GROUP BY m.film_id, m.movie_title, m.year_release;

CREATE TABLE users (
  user_id INT PRIMARY KEY,
  gender VARCHAR(1),
  yob INT,
  CAP INT,
  job_id INT,
  CHECK (gender IN ('M', 'F'))
);
CREATE INDEX idx_users_job_id ON users (job_id);

CREATE TABLE job (
  job_id INT,
  job_type VARCHAR(50),
  FOREIGN KEY (job_id) REFERENCES users (job_id)
);

CREATE TABLE ratings (
  UserID INT,
  MovieID INT,
  Rating INT,
  Timestamp_unix BIGINT,
  PRIMARY KEY (UserID, MovieID),
  FOREIGN KEY (UserID) REFERENCES users (user_id),
  FOREIGN KEY (MovieID) REFERENCES movies (film_id),
  CHECK (Rating BETWEEN 1 AND 5)
);

INSERT INTO users (user_id, gender, yob, CAP, job_id) VALUES
(1,'F',11,20023,0),
(2,'M',13,72022,0),
(3,'M',24,36100,1);

INSERT INTO job (job_id, job_type) VALUES
(0,'Studente'),
(1,'Impiegato');

INSERT INTO ratings (UserID, MovieID, Rating, Timestamp_unix) VALUES
(1,1,4,2147483647),
(1,2,5,2147483648),
(2,2,1,978301968);

SELECT * FROM users;
SELECT * FROM job;
SELECT * FROM ratings;
