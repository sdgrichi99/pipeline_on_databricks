{% macro promote_to_target(source_catalog, target_catalog) %}
  {{ log("Promozione tabelle da " ~ source_catalog ~ " a " ~ target_catalog ~ "...", info=True) }}

  {% set schemas_query %}
    SHOW SCHEMAS IN {{ source_catalog }}
  {% endset %}
  
  {% set schema_results = run_query(schemas_query) %}
  
  {% if execute %}
    {% for schema_row in schema_results %}
      {% set schema_name = schema_row[0] %}
      
      {# Esclude schemi di sistema ed elementary #}
      {% if schema_name not in ['information_schema', 'default', 'elementary'] %}
        {% do run_query("create schema if not exists " ~ target_catalog ~ "." ~ schema_name) %}
        
        {% set tables_query %}
          show tables in {{ source_catalog }}."{{ schema_name }}"
        {% endset %}
        {% set table_results = run_query(tables_query) %}
        
        {% for table_row in table_results %}
          {% set table_name = table_row[1] %}
          {% set promote_sql %}
            create or replace table {{ target_catalog }}."{{ schema_name }}"."{{ table_name }}" 
            clone {{ source_catalog }}."{{ schema_name }}"."{{ table_name }}";
          {% endset %}
          
          {% do run_query(promote_sql) %}
        {% endfor %}
        
      {% endif %}
    {% endfor %}
    {{ log("switch to qa completato", info=True) }}
  {% endif %}
{% endmacro %}