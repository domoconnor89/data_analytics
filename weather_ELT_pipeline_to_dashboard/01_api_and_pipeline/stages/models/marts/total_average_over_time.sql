with total_avg as (
    select 
        base_currency,
        avg(gbp) as avg_gbp,
        avg(usd) as avg_usd,
        avg(inr) as avg_inr
    from {{ref('prep_rates')}}
    group by base_currency
)

select *
from total_avg