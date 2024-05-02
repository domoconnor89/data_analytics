DROP TABLE IF EXISTS movies CASCADE;
CREATE TABLE movies (
    movieid INT primary key,
    title VARCHAR(255),
    genres VARCHAR(255),
    year INT);

\COPY movies FROM './data/movies.csv' DELIMITER ',' CSV HEADER ENCODING 'UTF8'


DROP TABLE IF EXISTS links CASCADE;
CREATE TABLE links (
    movieid INT REFERENCES movies(movieid),
    imdbId INT,
    tmdbId INT);

\COPY links FROM './data/links.csv' DELIMITER ',' CSV HEADER


DROP TABLE IF EXISTS ratings CASCADE;
CREATE TABLE ratings (
    userId INT,
    movieid INT REFERENCES movies(movieid),
    rating NUMERIC,
    time_stamp INT);

-- ALTER TABLE ratings FOREIGN KEY (movieid) REFERENCES movies(movieid);


\COPY ratings FROM './data/ratings.csv' DELIMITER ',' CSV HEADER



DROP TABLE IF EXISTS tags CASCADE;
CREATE TABLE tags (
    userId INT,
    movieid INT REFERENCES movies(movieid),
    tag  VARCHAR(255),
    timestamp INT);

\COPY tags FROM './data/tags.csv' DELIMITER ',' CSV HEADER

DROP TABLE IF EXISTS genres;
CREATE TABLE genres AS (
    SELECT 
    	movieid,
    	regexp_split_to_table(genres, '\|') AS genre
    FROM movies
);

-----------------------------------------------------------------------------------



-----------------------------------------------------------------------------------

-- to execute in terminal: psql -U postgres -p 5432 -h 34.141.104.250 -d movielens -f movielens.sql

-- DROP TABLE movies;
/* This returns the below ERROR MESSAGE, with the references in place for the 'movie_id' column and movie table...
... within each other table's movie_id column:

--  SQL Error [2BP01]: ERROR: cannot drop table movies because other objects depend on it
--  Detail: view drama_groups depends on table movies
--		view drama_movies depends on table movies
--  Hint: Use DROP ... CASCADE to drop the dependent objects too.		

------------------------------------------------------------------------------------------
Since the tables now have defined relationships between them a simple DROP TABLE will not suffice. 
--	CASCADE must be added. 
CASCADE will drop any of the contraints from one table on others in a cascading fashion. Add CASCADE to the relevant table(s):

	"DROP TABLE IF EXISTS table_name CASCADE;"

If everything is modeled correctly then the -f command should create the tables, fill them with data and apply the constraints:
--		psql -U postgres -p 5432 -h 34.141.104.250 -d movielens -f movielens.sql	--

To check if the foreign constraints have been applied review the output of the following command:
\d "table_name"

--	psql -U postgres -p 5432 -h 34.141.104.250 -d movielens
\d movies
\d ratings
\d links
\d tags

*/

