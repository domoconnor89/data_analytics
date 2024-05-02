WITH avg_vis as (
    SELECT 
        year,
        week,
        city,
        region,
        country,
        lat,
        lon,
        MAX(avgvis_km) as wk_maxvis_day,
        AVG(avgvis_km) as wkly_avg_vis,
        MIN(avgvis_km) as wk_minvis_day
    FROM {{ref('prep_temp')}}
    GROUP BY year, week, city, region, country, lat, lon
    ORDER BY city, year, week
)
SELECT *
FROM avg_vis