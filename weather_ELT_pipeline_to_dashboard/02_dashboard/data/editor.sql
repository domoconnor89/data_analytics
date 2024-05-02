
SELECT *
			FROM prep_temp
	LEFT JOIN wkly_avg_precip_by_city USING (city, region, country, lat, lon, year, week)
	LEFT JOIN mnthly_avg_precip_by_city USING (city, region, country, lat, lon, year, month)
	LEFT JOIN wkly_avg_temps_by_city USING (city, region, country, lat, lon, year, week)
	LEFT JOIN mnthly_avg_temps_by_city USING (city, region, country, lat, lon, year, month)
	LEFT JOIN wkly_avg_visibility_by_city USING (city, region, country, lat, lon, year, week)
	LEFT JOIN mnthly_avg_visibility_by_city USING (city, region, country, lat, lon, year, month)
	ORDER BY city, date;
	
SELECT *, SET (moonset_24hr - moonrise_24hr) as duration FROM daily_astro;


