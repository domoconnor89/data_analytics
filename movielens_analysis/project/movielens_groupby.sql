/* 1.How many ratings are available in the dataset?
- Display the total row count of the ratings table.
*/
SELECT * FROM ratings;
SELECT COUNT(*) FROM ratings; -- 100,818


/* 2.What is the distribution of genres combinations?
- Display the total count of different genres combinations in the movies table. 
*/ 
SELECT genres, COUNT(genres) AS number_of_movies FROM movies GROUP BY genres ORDER BY genres;


/* 3.Have you already explored the tags table? What unique tags can you see for a selected movie?
- Display unique tags for movie with id equal 60756. Use tags table.
*/
SELECT tag,COUNT(tag) FROM tags WHERE movieid = 60756 GROUP BY tag;
SELECT * FROM tags WHERE movieid = 60756;

/* 4.How many movies from different years do we have in the dataset? 
Focus only on given time period.
- Display the count of movies in the years 1990-2000 using the movies table. 
- Display year and movie_count.
*/
SELECT year, COUNT(year) FROM movies 
GROUP BY year HAVING year BETWEEN 1990 and 2000 
ORDER BY year;


/* 5.Which year had the highest number of movies in the dataset?
- Display the year where most of the movies in the database are from.
*/
SELECT year, COUNT(year) AS number_of_movies FROM movies 
GROUP BY year ORDER BY number_of_movies DESC 
LIMIT 1; -- 2002


/* 6.One of the metrics that could be used to measure the popularity of the movies 
is the total count of ratings (the number of people who rated a movie). 
What are the most popular movies if we use this metric?
- Display 10 movies with the most ratings. Use ratings table. 
- Display movieid, count_movie_ratings.
*/
SELECT movieid, COUNT(rating) As number_of_ratings FROM ratings 
GROUP BY movieid ORDER BY number_of_ratings DESC 
LIMIT 10;


/* 7.Another metric that we could use to measure the popularity of the movies is the average rating. 
However, to ensure the quality of this information we need to have at least a given number of ratings. 
What are the most popular movies using this metric?
- Display the top 10 highest rated movies by average that have at least 50 ratings. 
- Display the movieid, average rating and rating count. Use the ratings table.
*/


SELECT movieid, 
	COUNT(rating) As number_of_ratings,
	AVG(rating) As avg_ratings
		FROM ratings 
		GROUP BY movieid HAVING COUNT(rating) >= 50 
		ORDER BY avg_ratings DESC 
		LIMIT 10;

/*
SELECT movieid,  COUNT(rating) AS rating_count, AVG(rating) AS average_rating
FROM ratings
WHERE movieid IN (
    SELECT movieid
    FROM ratings
    GROUP BY movieid
    HAVING COUNT(rating) >= 50
)
GROUP BY movieid
ORDER BY average_rating DESC
LIMIT 10;
*/

/* 8.Imagine that you would like to continue focusing on the drama movies only. 
As you have multiple questions about drama movies you decided to create a view 
representing drama movies that you could reuse later on.
- Create a view that is a table of only movies that contain drama as one of it’s genres. 
- Display the first 10 movies in the view. 
*/

CREATE VIEW drama_groups AS
SELECT genres, COUNT(genres) AS count_of_movies FROM movies 
GROUP BY genres HAVING genres ILIKE '%drama%'
ORDER BY count_of_movies DESC
LIMIT 10;

CREATE VIEW drama_movies AS
SELECT * FROM movies WHERE genres ILIKE '%drama%' ORDER BY title LIMIT 10;

-- saved