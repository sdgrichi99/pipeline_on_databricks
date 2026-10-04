{% macro switch_to_target(source_catalog, target_catalog) %}
  {{ log("Avvio clonazione da " ~ source_catalog ~ " a " ~ target_catalog, info=True) }}

  {# 1. Recupera la lista degli schemi da clonare (escludendo quelli di sistema ed elementary) #}
  {% set schemas_query %}
    show schemas in {{ source_catalog }}
  {% endset %}
  
  {% set schema_results = run_query(schemas_query) %}
  
  {% if execute %}
    {% for schema_row in schema_results %}
      {% set schema_name = schema_row[0] %}
      
      {# Esclude schemi di sistema ed elementary #}
      {% if schema_name not in ['information_schema', 'default', 'elementary'] %}
        
        {# Crea lo schema nel catalogo temporaneo target se non esiste #}
        {% do run_query("create schema if not exists " ~ target_catalog ~ "." ~ schema_name) %}

        {% set tables_query %}
          select table_name 
          from {{ source_catalog }}.information_schema.tables 
          where table_schema = '{{ schema_name }}'
            and table_type in ('VIEW')
        {% endset %}
        
        {% set table_results = run_query(tables_query) %}
        
        {# 3. Esegue lo Shallow Clone per ciascuna tabella #}
        {% for table_row in table_results %}
          {% set table_name = table_row[0] %}
          
          {% if schema_name != 'elementary' or table_name == 'elementary_test_results' %}
          {% set clone_sql %}
            create or replace table {{ target_catalog }}.{{ schema_name }}.{{ table_name }}
            clone {{ source_catalog }}.{{ schema_name }}.{{ table_name }};
          {% endset %}
          {%endif %}
          
          {{ log("Clonazione tabella: " ~ schema_name ~ "." ~ table_name, info=True) }}
          {% do run_query(clone_sql) %}
        {% endfor %}
        
      {% endif %}
    {% endfor %}
    {{ log("Clonazione completata con successo", info=True) }}
  {% endif %}
{% endmacro %}