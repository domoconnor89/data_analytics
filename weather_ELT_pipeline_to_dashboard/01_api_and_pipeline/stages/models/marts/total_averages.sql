WITH avg_totals as (
    SELECT
        city,
        region,
        country,
        lat,
        lon,
        MAX(maxtemp_c) as overall_maxtemp,
        MIN(mintemp_c) as overall_mintemp,
        AVG(avgtemp_c) as overall_avgtemp,
        MAX(totalprecip_mm) as maxprecip_day_mm,
        SUM(rainy_day) as total_precip_days,
        SUM(totalprecip_mm) as overall_precip_mm,
        MAX(avgvis_km) as maxvis_day_km,
        AVG(avgvis_km) as overall_avg_vis_km,
        MIN(avgvis_km) as mnth_minvis_day_km
    FROM {{ref('prep_temp')}}
    GROUP BY city, region, country, lat, lon
    ORDER BY city
)
SELECT *
FROM avg_totals