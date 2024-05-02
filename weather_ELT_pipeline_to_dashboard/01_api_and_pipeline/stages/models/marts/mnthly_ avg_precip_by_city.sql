WITH mnth_avg_precip AS (
    SELECT 
        year,
        month,
        city,
        region,
        country,
        lat,
        lon,
        MAX(totalprecip_mm) as mnth_maxprecip_day,
        CAST(SUM(rainy_day) AS FLOAT) as mnthly_precip_days,
        SUM(totalprecip_mm) as mnth_totalprecip
    FROM {{ref('prep_temp')}}
    GROUP BY year, month, city, region, country, lat, lon
    ORDER BY city, year, month
),
update_mnthly_precip AS(
    SELECT
        *,
        CASE
            WHEN mnthly_precip_days > 0 THEN (1/mnthly_precip_days)
            WHEN mnthly_precip_days = 0 THEN 0
            END AS mnthly_rainfall_spread
    FROM mnth_avg_precip)
SELECT *
FROM update_mnthly_precip