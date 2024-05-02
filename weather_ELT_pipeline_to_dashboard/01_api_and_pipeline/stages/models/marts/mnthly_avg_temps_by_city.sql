WITH mnth_avg_temps as (
    SELECT 
        year,
        month,
        city,
        region,
        country,
        lat,
        lon,
        MAX(maxtemp_c) as mnthly_maxtemp,
        MIN(mintemp_c) as mnthly_mintemp,
        AVG(avgtemp_c) as mnthly_avgtemp
    FROM {{ref('prep_temp')}}
    GROUP BY year, month, city, region, country, lat, lon
    ORDER BY city, year, month
)
SELECT *
FROM mnth_avg_temps