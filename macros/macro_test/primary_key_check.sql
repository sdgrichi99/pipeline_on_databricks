{%- test primary_key_check(model, primary_key_list=[]) -%}

{%- set query %}
    select
        {{ primary_key_list | join (',') }},
        count(*) as num_rows
    from {{ model }}
    group by all
    having count(*) > 1
    order by 2 desc
{%- endset %}

{%- if execute %}
    {%- set results = run_query(query) %}
    {%- set key_length = results.columns[1].values() %}
{% else %}
    {% set key_length = [1] %}
{%- endif %}

{%- if key_length[0] > 1 %}
    {{ query }}
{%- else %}
    select 1 as key_length limit 0
{%- endif %}

{%- endtest -%}

