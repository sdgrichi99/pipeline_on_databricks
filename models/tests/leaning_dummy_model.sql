{% set input_data = 
    [
        ['01', 'computer'],
        ['02', 'stampante'],
        ['03', 'vaso'],
        ['01', 'computer']
    ]
%}

with dummy_data as (
    {%- for col in input_data %}
        {%- if not loop.first %} union all {% endif %}
            select
                '{{ col[0] }}' as product_id,
                '{{ col[1] }}' as product_name
    {%- endfor %}
)

select * from dummy_data