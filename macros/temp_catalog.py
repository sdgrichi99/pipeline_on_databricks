import argparse
import os
import sys
from databricks.sdk import WorkspaceClient


def main():
    parser = argparse.ArgumentParser(
        description="Gestione del catalogo temporaneo per PR su Databricks"
    )
    parser.add_argument(
        "--action",
        choices=["create", "drop"],
        required=True,
        help="Azione da eseguire: create o drop",
    )
    args = parser.parse_args()

    # Lettura delle variabili d'ambiente necessarie
    host = os.environ.get("DATABRICKS_HOST")
    token = os.environ.get("DATABRICKS_TOKEN")
    http_path = os.environ.get("DATABRICKS_HTTP_PATH")
    pr_num = os.environ.get("PR_NUM")

    if not all([host, token, http_path, pr_num]):
        print(
            "::error::Variabili d'ambiente mancanti. Assicurati che DATABRICKS_HOST, DATABRICKS_TOKEN, DATABRICKS_HTTP_PATH e PR_NUM siano impostate."
        )
        sys.exit(1)

    catalog_name = f"tst_pr_{pr_num}"
    warehouse_id = http_path.split("/")[-1]

    # Inizializzazione Client SDK Databricks
    w = WorkspaceClient(host=host, token=token)

    if args.action == "create":
        query = f"CREATE CATALOG IF NOT EXISTS {catalog_name}"
        print(f"creazione temp catalog: {catalog_name}...")
    elif args.action == "drop":
        query = f"DROP CATALOG IF EXISTS {catalog_name} CASCADE"
        print(f"eliminazione temp catalog: {catalog_name}...")

    try:
        response = w.statement_execution.execute_statement(
            statement=query, warehouse_id=warehouse_id
        )
        print(
            f"Operazione '{args.action}' completata con successo sul catalogo {catalog_name}!"
        )
    except Exception as e:
        print(f"::error::Errore durante l'esecuzione di '{args.action}': {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()