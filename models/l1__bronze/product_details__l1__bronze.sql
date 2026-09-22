with source_data as (
    select * from {{ source('loading_data', 'factory_details_prodotto')}}
),

final as (
    select
        id_azienda as azienda_id,
        settore_id,
        nome_settore,
        responsabile_settore,
        prodotto_id,
        categoria as categoria_prodotto,
        nome_prodotto,
        ordine_id,
        riga_id,
        nome_file_origine,
        file_loading_dtm
    from source_data
)

select * from final