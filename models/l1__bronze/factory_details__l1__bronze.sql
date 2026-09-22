with source_data as (
    select * from {{ source('loading_data', 'factory_details_root_summaries')}}
),

final as (
    select
        id_azienda as azienda_id,
        azienda as nome_azienda,
        estrazione_timestamp,
        nome_file_origine,
        file_loading_dtm
    from source_data
)

select * from final