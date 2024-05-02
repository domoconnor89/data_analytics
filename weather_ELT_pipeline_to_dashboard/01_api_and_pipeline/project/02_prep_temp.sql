WITH temp_daily AS (
    SELECT * 
    FROM {{ref('staging_weather')}}
),
time_cnvrt AS (
    SELECT *,
        TO_CHAR(date,'Day') AS weekday,
        TO_CHAR(date,'DD') AS day_num,
        date_part('week', date) AS week,
        date_part('month', date) AS month,
        date_part('year', date) AS year,
        REPLACE (moonrise, 'No moonrise', '11:59 PM') as moonrise_mid,
        REPLACE (moonset, 'No moonset', '11:59 PM') as moonset_mid,
        CAST(moon_illumination AS INTEGER) AS moon_illumination_num,
        CASE
            WHEN totalprecip_mm > 0 THEN 1
            WHEN totalprecip_mm = 0 THEN 0
            END AS rainy_day
    FROM temp_daily
),
temp_update AS (
    SELECT 
        date,
        weekday,
        day_num,
        week,
        month,
        year,
        city,
        region,
        country,
        lat,
        lon,
        TO_CHAR(TO_TIMESTAMP(sunrise, 'HH12:MI PM'), 'HH24:MI') AS sunrise_24hr,
        TO_CHAR(TO_TIMESTAMP(sunset, 'HH12:MI PM'), 'HH24:MI') AS sunset_24hr,
        TO_CHAR(TO_TIMESTAMP(moonrise_mid, 'HH12:MI PM'), 'HH24:MI') AS moonrise_24hr,
        TO_CHAR(TO_TIMESTAMP(moonset_mid, 'HH12:MI PM'), 'HH24:MI') AS moonset_24hr,
        moon_phase,
        moon_illumination_num,
        maxtemp_c,
        avgtemp_c,
        mintemp_c,
        maxwind_kph,
        totalprecip_mm,
        rainy_day,
        avgvis_km,
        avghumidity,
        condition
    FROM time_cnvrt
)
SELECT *
FROM temp_update