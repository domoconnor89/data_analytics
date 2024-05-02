	-- The ratings of 'Tarantino' tagged films:
DROP TABLE IF EXISTS qt;
CREATE VIEW qt AS (
SELECT title, MIN(year) AS released, AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
	SELECT movies.movieid, movies.title, tags.tag, movies.year, ratings.rating
		FROM movies 
			LEFT JOIN tags ON tags.movieid = movies.movieid
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
				WHERE tag ILIKE '%tarantino')AS qt
					GROUP BY title
					ORDER BY avg_rating DESC);
SELECT * FROM qt;
-------------------- missing Kill Bill and Jackie Brown --------------------
DROP TABLE IF EXISTS tarantino;
CREATE TABLE tarantino AS (
SELECT title, released, avg_rating, rating_count FROM qt
	UNION
SELECT title, released, avg_rating, rating_count FROM(
SELECT title AS title, MIN(year) AS released, AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM (
	SELECT movies.movieid, movies.title, movies.year, ratings.rating 
		FROM movies FULL JOIN ratings USING (movieid) 
		WHERE (title ILIKE '%kill bill%' OR title ILIKE '%jackie brown%')) AS kb GROUP BY title ORDER BY avg_rating DESC) AS tar);
SELECT * FROM tarantino ORDER BY released;

/*
- high vol rating count for 1st movie, peaking for 2nd, then progressively fewer with big drop-off for latest.
- progressively lower ratings for more recent movies, with 

- Balance between audience fatigue and return boost?
- Is this consistent with other highly stylised directors and franchises?
*/
--------------------------------------------------------------------------------------------------

	-- The ratings of 'Scorsese' tagged films:
DROP TABLE IF EXISTS scorsese;
CREATE TABLE scorsese AS (
SELECT title, MIN(year) AS released, AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
SELECT movies.movieid, movies.title, tags.tag, movies.year, ratings.rating
		FROM movies 
			LEFT JOIN tags ON tags.movieid = movies.movieid
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
				WHERE tag ILIKE '%Scorsese%')AS ms
					GROUP BY title
					ORDER BY avg_rating DESC);
Select * FROM scorsese;

SELECT title, released, AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
SELECT movies.movieid, movies.title, tags.tag, movies.year AS released, ratings.rating
		FROM movies 
			LEFT JOIN tags ON tags.movieid = movies.movieid
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
				WHERE (tag ILIKE '%Scorsese%') 
					OR 
				(title ILIKE '%taxi driver%' OR title ILIKE '%irishman%' OR title ILIKE '%mean streets%' OR title ILIKE '%aviator%'
				 OR title ILIKE '%goodfellas%' OR title ILIKE '%king of comedy, the' OR title ILIKE '%raging bull%')) AS ms
					GROUP BY title, released
					ORDER BY avg_rating DESC;

/*
- When only searching with tags, similar to Tarantino: progressively lower ratings for more recent movies, except for the earliest film

Departed / 2006 / 4.25 / 107
Shutter Island / 2010 / 4.02 / 67
Wolf of Wall St / 2013 / 3.91 / 54
Cape Fear / 1991 / 3.78 / 25

- after adding-in a lot of missing notable movies, any supposed correlation dissipates

tags for directors not the best for searching movies but let's try another...
*/
--------------------------------------------------------------------------------------------------

		-- The ratings of 'Hitchcock' tagged films
SELECT title, MIN(year) AS released, AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
SELECT movies.movieid, movies.title, tags.tag, movies.year, ratings.rating
		FROM movies 
			LEFT JOIN tags ON tags.movieid = movies.movieid
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
				WHERE tag ILIKE '%Hitchcock')AS ah
					GROUP BY title
					ORDER BY avg_rating DESC;
-------------------- very few films tagged --------------------
------------- filter with specific titles and year ------------
SELECT title, MIN(year) AS released, AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
SELECT movies.movieid, movies.title, tags.tag, movies.year, ratings.rating
		FROM movies 
			LEFT JOIN tags ON tags.movieid = movies.movieid
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
	WHERE (title ILIKE 'psycho%' OR title ILIKE '%vertigo%'
	OR title ILIKE '%birds%' OR title ILIKE '%rear window%' OR title ILIKE '%vertigo%'
	OR title ILIKE '%north by northwest%' OR title ILIKE '%rebecca%' OR title ILIKE '%wrong man%'
	OR title ILIKE '%strangers on a train%' OR title ILIKE '%man who knew too much%' OR title ILIKE '%for murder%')
	AND year <= 1965)AS ah GROUP BY title ORDER BY avg_rating DESC;
	
/*	
- Very little obvious correlation.
- Hitchcock's catalogue of films is extensive so creating a table this way is not so representative...
		---------------------- https://www.imdb.com/list/ls033850629/ ----------------------
- Would be interesting to check trends through full list but will need to find a more efficient way to search 56x titles
 
What about movie franchises?
*/	

	-- The ratings of 'Marvel' tagged films
SELECT title, MIN(year) AS released, AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
SELECT movies.movieid, movies.title, tags.tag, movies.year, ratings.rating
		FROM movies 
			LEFT JOIN tags ON tags.movieid = movies.movieid
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
				WHERE (tag ILIKE '%marvel%')
					OR (title NOT LIKE '%Nobody Speak: Hulk Hogan, Gawker and Trials of a Free Press%' AND
					title ILIKE '%x-men%' OR title ILIKE '%x men%' OR title ILIKE '%hulk%' 
					OR title ILIKE '%fantastic four%' OR title ILIKE 'avengers' 
					OR title ILIKE '%ironman%' OR title ILIKE '%iron man%' OR title ILIKE '%iron-man%')
					AND (year > 1989)
					)AS mrvl
						GROUP BY title
						ORDER BY rating_count DESC;
/*	
- When only searching with 'Marvel' tag, slight correlation between release year and avg rating. 
However, greatest interest in first film (highest count number) which reduces with each release.

- But again, after adding-in a lot of missing notable movies, any supposed correlation disapears.
This is even the case for specific movie series... x-men, for example.
*/
		
		-- The ratings of 'pirates of the caribbean' films

SELECT title, MIN(year) AS released, AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
SELECT movies.movieid, movies.title, movies.year, ratings.rating
		FROM movies 
			LEFT JOIN tags ON tags.movieid = movies.movieid
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
				WHERE title ILIKE '%pirates of the caribbean%')AS pc
					GROUP BY title
					ORDER BY avg_rating DESC;
/*
- Follows the fatigue theory with progressively lower and fewer ratings for more recent movies...
-... with exception for the most recent, which is highest rated but significantly fewer ratings.
- highest rating count for 1st movie, with large drop-off thereafter; no peak for 2nd.
 */			
--------------------------------------------------------------------------------------------------
	-- Harry Potter (8x Movies found):
SELECT title, MIN(year) AS released, AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
SELECT movies.movieid, movies.title, movies.year, ratings.rating
		FROM movies
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
				WHERE title ILIKE 'harry potter%')AS dh
					GROUP BY title
					ORDER BY rating_count DESC;
/*				
- Generally more favorable ratings for the more recent movies but higher volume of reviews for the earlier films.
- high vol rating count for 1st movie, peaking for 2nd, then progressively fewer until levelling-out for last few.
*/
--------------------------------------------------------------------------------------------------
		-- The ratings of 'Bond' films
				
DROP VIEW IF EXISTS b007nd;
CREATE VIEW b007nd AS (
SELECT title, MAX(year) AS released, AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
SELECT movies.movieid, movies.title, movies.year, ratings.rating
		FROM movies
			LEFT JOIN ratings ON ratings.movieid = movies.movieid
	WHERE title ILIKE 'Dr. No%' OR title ILIKE 'From Russia with Love%'
	OR title ILIKE '%Goldfinger%' OR title ILIKE '%Thunderball%' OR title ILIKE '%You Only Live Twice%'
	OR title ILIKE '%On Her Majesty''s Secret Service%' OR title ILIKE 'Diamonds Are Forever' OR title ILIKE '%Live and Let Die%'
	OR title ILIKE '%Man with the Golden Gun%' OR title ILIKE '%Spy Who Loved Me%' OR title ILIKE '%Moonraker%'
	OR title ILIKE '%For Your Eyes Only%' OR title ILIKE '%Octopussy%' OR title ILIKE '%Never Say Never Again%' 
	OR title ILIKE '%A View to a Kill%' OR title ILIKE '%Living Daylights%' OR title ILIKE '%Licence to Kill%'
	OR title ILIKE '%GoldenEye%' OR title ILIKE '%Tomorrow Never Dies%' OR title ILIKE '%World Is Not Enough%' 
	OR title ILIKE '%Die Another Day%' OR title ILIKE '%Quantum of Solace%' 
	OR title ILIKE '%Skyfall%' OR title ILIKE '%Spectre%' OR title ILIKE '%No Time to Die%'  
	)AS bond GROUP BY title ORDER BY avg_rating DESC);
SELECT * FROM b007nd;
----------------------- ADD BOTH CASINO ROYALE FILMS -----------------------
DROP TABLE IF EXISTS bond;
CREATE TABLE bond AS (
SELECT title, released, avg_rating, rating_count FROM b007nd
	UNION
SELECT title, released, avg_rating, rating_count FROM(
SELECT MIN(title) AS title, year AS released, AVG(rating) AS avg_rating,COUNT(rating) AS rating_count FROM(
	SELECT movies.movieid, movies.title, movies.year, ratings.rating 
		FROM movies FULL JOIN ratings USING (movieid) 
		WHERE title ILIKE '%Casino royal%') AS cr GROUP BY year) AS cas ORDER BY released);
SELECT * FROM bond;
/*
- Audience fatigue appears more fitting for the eras of each actor, with noticebale negative reaction to short-lived Bonds:

 * Sean Connery – 1962 - 1967 (Dr. No ... You Only Live Twice).
 * David Niven – 1967 (Casino Royale).
 * George Lazenby – 1969 (On Her Majesty's Secret Service).
 * Sean Connery - 1971 (Diamonds Are Forever)***
 * Roger Moore – 1973 - 1985 (Live and Let Die ... Octopussy / A View to a Kill).
 * Sean Connery - 1983 (Never Say Never Again)
 * Timothy Dalton – 1987 - 1989 (Living Daylights ... Licence to Kill).
 * Pierce Brosnan – 1995 - 2002 (GoldenEye ... Die Another Day).
 * Daniel Craig – 2006 - 2021 (Casino Royale  ... Spectre).
 
--------------------------------------------------------------------------------------------------

Is it possible to see if audience fatigue exists using this data... no.

But it would be an interesting topic to look into with a more thorough dataset... 
- pair with critic ratings
- potential to cluster the directors who do / don't suffer from this
- any trends for directors with long careers / breaks in their careers / varied genre catalogue...

 */
