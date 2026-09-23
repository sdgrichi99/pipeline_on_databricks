with source_data as (
    select * from {{ source('loading_data', 'factory_details_ordini')}}
),

final as (
    select 
        id_azienda as azienda_id,
        ordine_id,
        data_ordine,
        importo_totale,
        valuta,
        canale_vendita,
        file_loading_dtm,
        nome_file_origine
    from source_data
)

select * from final