-------------- Practice CTE --------------
-- Write a CTE query with following steps:
SELECT * FROM weather;

-- 1. Show weekly average temp for each location
--             Tip: group by calendar week number and location

WITH date_splits AS(
	SELECT *, date_part('month', date) AS month, date_part('year', date) AS year
			FROM weather)
, avg_wk_temp AS(
	SELECT date_part('week', date) AS week, 
		city, 
		country, 
		AVG(avgtemp_c) AS avg_temp
			FROM weather 
		GROUP BY week, city, country
	)
SELECT * FROM avg_wk_temp ORDER BY country, city, week;

-- 2. Show max weekly average, highest and lowest temperatures per month for each location
--             Tip: group by month and location
WITH date_splits AS(
	SELECT *, date_part('month', date) AS month, date_part('year', date) AS year
			FROM weather)
, avg_temps AS(
	SELECT date_part('week', date) AS week,
		date_part('month', date) AS month,
		date_part('year', date) AS year, 
		city, 
		country, 
		AVG(avgtemp_c) AS avg_wk_temp,
		AVG(maxtemp_c) AS max_wk_temp,
		AVG(mintemp_c) AS min_wk_temp
			FROM weather 
			GROUP BY year, month, week, city, country
	)
, mnthly_temps AS(
	SELECT 
		month
		,year
		,country
		,city
		,MAX(avg_wk_temp)AS max_avg_wk_temp
		,MAX(max_wk_temp)AS max_max_wk_temp
		,MAX(min_wk_temp)AS max_min_wk_temp
			FROM avg_temps
			GROUP BY month, year, country, city
			ORDER BY country, city, year, month
	)
SELECT * FROM mnthly_temps;

-- 3. Join results from Step 1. and Step 2. to the original daily data.
--             Tip: In original table, add missing features on which th temporary named result sets will be join on

WITH date_splits AS(
	SELECT *,
		date_part('year', date) AS year,
		date_part('month', date) AS month,
		date_part('week', date) AS week
			FROM weather),
avg_temps AS(
	SELECT week,
		month,
		year, 
		city, 
		country, 
		AVG(maxtemp_c) AS max_wk_temp,
		AVG(avgtemp_c) AS avg_wk_temp,
		AVG(mintemp_c) AS min_wk_temp
			FROM date_splits 
			GROUP BY year, month, week, city, country
	)
, mnthly_temps AS(
	SELECT 
		month
		,year
		,country
		,city
		,MAX(max_wk_temp)AS max_Months_week_maxtemp
		,MAX(avg_wk_temp)AS max_Months_week_avgtemp
		,MAX(min_wk_temp)AS max_Months_week_mintemp
			FROM avg_temps
			GROUP BY month, year, country, city
			ORDER BY country, city, year, month
	)
SELECT *
			FROM date_splits
	LEFT JOIN avg_temps USING (city, country, year, month, week)
	LEFT JOIN mnthly_temps USING (city, country, year, month)
	ORDER BY country, city, date;

SELECT * FROM weather;
