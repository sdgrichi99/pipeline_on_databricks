with source_data as (
    select * from {{ source('loading_data', 'factory_details_pagamenti')}}
),

final as (
    select
        id_azienda as azienda_id, 
        ordine_id,
        transazione_id,
        metodo_pagamento,
        stato_pagamento,
        circuito,
        importo_pagato,
        nome_file_origine,
        file_loading_dtm
    from source_data
)

select * from final