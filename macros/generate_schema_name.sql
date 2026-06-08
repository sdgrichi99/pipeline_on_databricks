{% macro generate_schema_name(custom_schema_name, node) %}
    {# Prende lo schema di default del target nel profilo dbt #}
    {% set default_schema = target.schema %}
    
    {%- if custom_schema_name is none %}
        {%- set schema_name = default_schema %}
    {%- else %}
        {%- set schema_name = custom_schema_name | trim %}
    {%- endif %}

    {%- if execute -%}
        {%- set query_schema_check %}
            select 1
            from {{ node.database }}.information_schema.schemata
            where lower(schema_name) = lower('{{ schema_name }}')
        {%- endset -%}

        {%- set results = run_query(query_schema_check) -%}
        {{ log("Righe trovate: " ~ results.rows | length, info=True) }}
        {%- if results.rows | length == 0 -%}
            {%- set err_msg = "The model '" ~ node.name ~ "' needs the schema '" ~ schema_name ~ "', to be created in the catalog'" ~ node.database ~ "'" -%}
            {{ exceptions.raise_compiler_error(err_msg) }}
        {%- endif -%}
    {%- endif -%}

    {{ schema_name }}

{% endmacro %}