WITH mnth_avg_vis as (
    SELECT 
        year,
        month,
        city,
        region,
        country,
        lat,
        lon,
        MAX(avgvis_km) as mnth_maxvis_day,
        AVG(avgvis_km) as mnthly_avg_vis,
        MIN(avgvis_km) as mnth_minvis_day
    FROM {{ref('prep_temp')}}
    GROUP BY year, month, city, region, country, lat, lon
    ORDER BY city, year, month
)
SELECT *
FROM mnth_avg_vis