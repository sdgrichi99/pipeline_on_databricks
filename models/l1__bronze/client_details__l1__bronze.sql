with source_data as (
    select * from {{ source('loading_data', 'factory_details_cliente')}}
),

final as (
    select 
        id_azienda as azienda_id,
        ordine_id,
        cliente_id,
        nome as nome_cliente,
        cognome as cognome_cliente,
        email as email_cliente,
        indirizzo_paese,
        indirizzo_citta,
        segmento as tipologia_cliente,
        nome_file_origine,
        file_loading_dtm
    from source_data
)

select * from final