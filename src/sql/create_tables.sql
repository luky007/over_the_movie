-- Create the tables in the db.
CREATE TABLE movies (
  movie_id INT PRIMARY KEY,
  movie_title VARCHAR(255),
  movie_original_title VARCHAR(255),
  year_release INT
);
CREATE INDEX idx_movie_title ON movies (movie_title);

CREATE TABLE genres (
  genre_id INT PRIMARY KEY,
  genre VARCHAR(50)
);

CREATE TABLE movies_genres_link (
  movie_id INT,
  genre_id INT,
  FOREIGN KEY (movie_id) REFERENCES movies (movie_id),
  FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
);

CREATE TABLE users (
  user_id INT PRIMARY KEY,
  gender VARCHAR(1),
  age INT,
  cap INT,
  job_id INT,
  CHECK (gender IN ('M', 'F'))
);
CREATE INDEX idx_users_job_id ON users (job_id);

CREATE TABLE jobs (
  job_id INT,
  job_type VARCHAR(50),
  FOREIGN KEY (job_id) REFERENCES users (job_id)
);

CREATE TABLE ratings (
  user_id INT,
  movie_id INT,
  rating INT,
  timestamp_unix BIGINT,
  PRIMARY KEY (user_id, movie_id),
  FOREIGN KEY (user_id) REFERENCES users (user_id),
  FOREIGN KEY (movie_id) REFERENCES movies (movie_id),
  CHECK (rating BETWEEN 1 AND 5)
);
