with source_data as (
    select * from {{ source('loading_data', 'factory_details_dettagli_ordine')}}
),

final as (
    select 
        id_azienda as azienda_id,
        ordine_id,
        riga_id,
        prezzo_unitario,
        quantita,
        sconto_applicato,
        nome_file_origine,
        file_loading_dtm
    from source_data
)

select * from final