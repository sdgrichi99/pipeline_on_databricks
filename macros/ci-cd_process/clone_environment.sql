{% macro clone_environment(source_catalog, target_catalog) %}
  {{ log("Avvio clonazione da " ~ source_catalog ~ " a " ~ target_catalog, info=True) }}

  {#Recupera lista di tutti gli schemi del catalogo sorgente #}
  {% set schemas_query %}
    show schemas in {{ source_catalog }}
  {% endset %}
  
  {% set schema_results = run_query(schemas_query) %}
  
  {% if execute %}
    {% for schema_row in schema_results %}
      {% set schema_name = schema_row[0] %}
      
      {# Esclude schemi di sistema #}
      {% if schema_name not in ['information_schema', 'default'] %}
        
        {# Crea lo schema nel catalogo temporaneo se non esiste #}
        {% do run_query("create schema if not exists " ~ target_catalog ~ "." ~ schema_name) %}
        
        {# 2. Recupera le tabelle presenti nello schema #}
        {% set tables_query %}
          show tables in {{ source_catalog }}.{{ schema_name }}
        {% endset %}
        {% set table_results = run_query(tables_query) %}
        
        {# 3. Esegue lo Shallow Clone per ciascuna tabella #}
        {% for table_row in table_results %}
          {% set table_name = table_row[1] %}
          {% set clone_sql %}
            create or replace table {{ target_catalog }}.{{ schema_name }}.{{ table_name }}
            shallow clone {{ source_catalog }}.{{ schema_name }}.{{ table_name }};
          {% endset %}
          
          {% do run_query(clone_sql) %}
        {% endfor %}
        
      {% endif %}
    {% endfor %}
    {{ log("Clonazione completata con successo!", info=True) }}
  {% endif %}
{% endmacro %}