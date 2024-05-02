-- Connect to the movielens database. Select the genres column to inspect the data:
SELECT genres FROM movies LIMIT 5;

/*
	Step 2: Split the genres
To map each indivdual movie to a genres the "regexp_split_to_table(column, 'pattern')" can be used. 
The first argument is the column on which to execute the function...
... and the second the pattern to split the string with:

SELECT movieid, regexp_split_to_table(genres, '\|') FROM movies;

*/

SELECT movieid, regexp_split_to_table(genres, '\|') FROM movies LIMIT 10;

-- The resulting table is each genre being mapped to the corresponding movieid. 
	-- Having a table like this to refer to will help filter results by specific genres.

/*
	Step 3: Create a genres tables
The table above is only a result of the query. In order to store as a DERIVED TABLE 
the following code can either be executed in the psqlshell or added to the movie_lens.sql and run with the -f argument:
*/

DROP TABLE IF EXISTS genres;
CREATE TABLE genres AS (
    SELECT 
    	movieid,
    	regexp_split_to_table(genres, '\|') AS genre
    FROM movies
);

ALTER TABLE genres
	ADD FOREIGN KEY (movieid) REFERENCES movies(movieid);

SELECT * FROM genres;
--------------------------------------------------------------------------------------------------------------------

-- 1. Using a JOIN display 5 movie titles with the lowest imdb ids
		-- CHECK THE TABLES (and format the "links" table to match the final display)...
SELECT * FROM links ORDER BY imdbid LIMIT 5;
SELECT * FROM movies;

			-- EXECUTE...
SELECT movies.title, links.movieid, links.imdbid
	FROM links LEFT JOIN movies USING (movieid)
	ORDER BY imdbid LIMIT 5;


-- 2. Display the count of drama movies
		-- display table info...
SELECT * FROM genres;

			--EXECUTE...
SELECT genre, COUNT(genre) FROM genres GROUP BY genre 
	HAVING genre ILIKE '%drama%'; -- 4359 (same with/out % wildcard)


-- 3. Using a JOIN display all of the movie titles that have the tag fun
		-- display table...
SELECT * FROM tags WHERE tag ILIKE 'fun';

			--EXECUTE...
SELECT movies.movieid, movies.title, tags.tag, tags.userid
	FROM tags LEFT JOIN movies USING (movieid) 
	WHERE tag ILIKE 'fun';


-- 4. Using a JOIN find out which movie title is the first without a tag
SELECT movies.movieid, movies.title, tags.tag
	FROM tags RIGHT JOIN movies USING (movieid) 
	WHERE tag IS NULL
	ORDER BY movieid LIMIT 5;


-- 5. Using a JOIN display the top 3 genres and their average rating
		-- display table info...
SELECT * FROM genres;
SELECT * FROM ratings;
SELECT movieid, AVG(rating) AS avg_rating FROM ratings GROUP BY movieid ORDER BY avg_rating DESC;

			-- EXECUTE... using sub-query
SELECT genre, AVG(rating) AS avg_rating FROM (
	SELECT genres.genre,  ratings.rating
	FROM genres LEFT JOIN ratings USING (movieid)) AS r 
		GROUP BY genre 
		ORDER BY AVG(rating) DESC 
		LIMIT 10;


-- 6. Using a JOIN display the top 10 movie titles by the number of ratings
		-- display table info...
SELECT * FROM movies;
SELECT movieid, COUNT(rating) AS rating_count FROM ratings GROUP BY movieid ORDER BY rating_count DESC LIMIT 10;

			-- EXECUTE... using sub-query
SELECT title, COUNT(rating) AS rating_count FROM (
	SELECT movies.movieid, movies.title, ratings.rating FROM ratings LEFT JOIN movies USING (movieid)) AS r
		GROUP BY title
		ORDER BY rating_count DESC
		LIMIT 10;


-- 7. Using a JOIN display all of the Star Wars movies in order of average rating where the film was rated by at least 40 users
		-- display table info...
SELECT * FROM movies WHERE title ILIKE '%star wars%';
SELECT movieid, AVG(rating), COUNT(rating) FROM ratings GROUP BY movieid HAVING COUNT(rating)>= 40 ORDER BY AVG(rating) DESC;

			-- EXECUTE
SELECT title, AVG(rating) AS avg_rating, COUNT(rating) AS rating_count FROM (
	SELECT movies.movieid, movies.title, ratings.rating 
	FROM ratings RIGHT JOIN movies USING (movieid) 
	WHERE title ILIKE '%star wars%') AS r
		GROUP BY title
		HAVING COUNT(rating)>= 40
		ORDER BY avg_rating DESC;


-- 8. Create a derived table from one or more of the above queries
			-- Tarantino Table
CREATE TABLE tarantino AS (
SELECT title, MIN(year), AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
	SELECT movies.movieid, movies.title, tags.tag, movies.year, ratings.rating
		FROM movies 
			LEFT JOIN tags ON tags.movieid = movies.movieid
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
				WHERE tag ILIKE '%tarantino')AS qt
					GROUP BY title
					ORDER BY avg_rating DESC);

-- progressively lower ratings for more recent movies
-- high vol rating count for 1st movie, peaking for 2nd, then progressively fewer

				
		-- Martin Scorsese
SELECT title, MIN(year), AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
SELECT movies.movieid, movies.title, tags.tag, movies.year, ratings.rating
		FROM movies 
			LEFT JOIN tags ON tags.movieid = movies.movieid
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
				WHERE tag ILIKE '%Scors%')AS ms
					GROUP BY title
					ORDER BY avg_rating DESC;
				
				
		-- Alfred Hitchcock	
SELECT title, MIN(year), AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
SELECT movies.movieid, movies.title, tags.tag, movies.year, ratings.rating
		FROM movies 
			LEFT JOIN tags ON tags.movieid = movies.movieid
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
				WHERE tag ILIKE '%Hitchcock%')AS ms
					GROUP BY title
					ORDER BY avg_rating DESC;

			
SELECT title, MIN(year), AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
SELECT movies.movieid, movies.title, tags.tag, movies.year, ratings.rating
		FROM movies 
			LEFT JOIN tags ON tags.movieid = movies.movieid
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
				WHERE tag ILIKE '%Spielberg%')AS ms
					GROUP BY title
					ORDER BY avg_rating DESC;

SELECT title, MIN(year), AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
SELECT movies.movieid, movies.title, tags.tag, movies.year, ratings.rating
		FROM movies 
			LEFT JOIN tags ON tags.movieid = movies.movieid
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
				WHERE tag ILIKE '%coppola%')AS ms
					GROUP BY title
					ORDER BY avg_rating DESC;
				
SELECT title, MIN(year), AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
SELECT movies.movieid, movies.title, tags.tag, movies.year, ratings.rating
		FROM movies 
			LEFT JOIN tags ON tags.movieid = movies.movieid
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
				WHERE tag ILIKE '%depp')AS ms
					GROUP BY title
					ORDER BY avg_rating DESC;

