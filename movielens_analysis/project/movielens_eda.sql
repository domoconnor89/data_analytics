/* 
1.What is the data structure? What information do we have available for movies?
-- Display the (whole) movies table. 
 */

SELECT * FROM movies;
SELECT COUNT(*) FROM movies; -- From 'movies' tale: Title / Genres / Year of Release (9,729 rows)
SELECT * FROM ratings;
SELECT COUNT(*) FROM ratings; -- User Ratings from 'ratings' table (100,818 rows)
SELECT * FROM tags;
SELECT COUNT(*) FROM tags; -- Ascociated Key Words / Tags from 'tags' table (3,680 rows)


/* 2.In the movies table there is a field called movieId. 
Sometimes we will not need this field for the analysis. 

--Display only title and genres of the first 10 entries from the movies table that is sorted...
... alphabetically (starting from A) by the movie titles.
*/

SELECT title,genres,year FROM movies ORDER BY title LIMIT 10 ;


/* 3.How many movies do we have the data for?
-- Display the total row count */

SELECT COUNT(*) FROM movies; -- 9,729

/* 4.Every movie has a genre assign to it. Maybe you have noticed that some of the movies 
 * have a few different genres assigned to them. 
 * Let’s pick one of the genres - e.g. drama - and check how many movies we have that were classified as this genre only.

-- Display first 10 pure Drama movies. Only Drama is in the genre column.
-- Display the count of pure Drama movies.*/

SELECT COUNT(*) FROM movies WHERE genres ILIKE 'drama' -- 1052


/* 5.Some of the movies are classified as a combination of a few genres. Check how many movies have drama as one of the assigned genres.
-- Display the count of drama movies that can also contain other genres. 
-- Is this number different from the one in the previous question? Why do you think so? */

SELECT COUNT(*) FROM movies WHERE genres ILIKE '%drama%' -- 4359


/* 6.What is the count of movies that are not classified as drama movies?
-- Display the count of movies don’t have drama (in any combination) as assigned genre */

SELECT COUNT(*) FROM movies WHERE genres NOT ILIKE '%drama%' -- 5370

/* 7.Do you have a favorite film? Which year is it from? 
 * How many movies from this year are visible in the movies dataset?
 * */

SELECT * FROM movies ORDER BY year DESC;
SELECT * FROM movies WHERE title ILIKE '%superbad%';
SELECT COUNT(*) FROM movies WHERE year = 2007; -- 284


/* 8.Do we have more movies from recent years? Do we have any movies from earlier years?
-- Find all movies with a year lower 1910. */

SELECT COUNT(*) FROM movies WHERE year >= 2008; -- 2,482
SELECT COUNT(*) FROM movies WHERE year <= 2006; -- 6,963
SELECT * FROM movies WHERE year <= 1910; -- 3


/* 9.Have you ever watched Star Wars? Or is there a different series of movies that you loved. 
 * Let’s see which of these movies are in the dataset.
-- Retrieve all Star Wars movies from the movie table. */

SELECT COUNT(*) FROM movies WHERE title ILIKE '%star%war%'; -- 13
SELECT * FROM movies WHERE title ILIKE '%star%war%' ORDER BY year;
