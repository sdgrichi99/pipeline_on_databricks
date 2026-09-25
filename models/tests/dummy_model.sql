with final as (
    select * from {{ ref('leaning_dummy_model') }}
)

select * from final