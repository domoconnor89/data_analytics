WITH daily_astro AS (
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
        sunrise_24hr,
        sunset_24hr,
        moonrise_24hr,
        moonset_24hr,
        moon_phase,
        moon_illumination_num,
        condition
    FROM {{ref('prep_temp')}}
    ORDER BY city, date
)
SELECT *
FROM daily_astro