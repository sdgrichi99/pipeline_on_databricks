{%- test source_data_validation(model, source_model, id_fields = []) %}

with source_data as (
    select {{ id_fields | join(',')}}
    from {{ source_model }}
),

model as (
    select {{ id_fields | join(',')}}
    from {{ model }}
)

select {{ id_fields | join(',')}}
from model
where not exists (
    select *
    from source_data
    where 
    {%- for field in id_fields %}
        {%- if not loop.first %} and {% endif %}
            model.{{ field }} = source_data.{{ field }}
    {%- endfor %}
)

{% endtest %}