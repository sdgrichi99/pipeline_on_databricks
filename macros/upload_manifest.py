import os
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound

DEFAULT_VOLUME = "/Volumes/workspace_prod/default/dbt_artifacts/manifest.json"

def upload_manifest():
    local_file = os.path.join("target", "manifest.json")
    volume_path = os.environ.get("DBT_MANIFEST_VOLUME_PATH", DEFAULT_VOLUME)

    print("=== dbt Manifest Uploader ===")
    print(f"File locale da caricare: {local_file}")
    print(f"Destinazione Volume Databricks: {volume_path}")

    if not os.path.exists(local_file):
        raise FileNotFoundError(f"Errore: Il file {local_file} non esiste. Assicurati che 'dbt compile' sia stato eseguito con successo.")

    # Recupero credenziali con fallback
    host = os.environ.get("DATABRICKS_HOST")
    token = os.environ.get("DATABRICKS_TOKEN") or os.environ.get("DBT_ACCESS_TOKEN")

    try:
        if host and token:
            w = WorkspaceClient(host=host, token=token)
        else:
            w = WorkspaceClient()

        print("Caricamento del file manifest su Databricks Volume in corso...")
        
        with open(local_file, "rb") as f:
            # overwrite=True permette di sostituire il vecchio manifest.json
            w.files.upload(volume_path, f, overwrite=True)
            
        print("Manifest aggiornato e caricato con successo sul Volume Databricks!")

    except Exception as e:
        print(f"Errore critico durante l'upload del manifest: {str(e)}")
        raise e

if __name__ == "__main__":
    upload_manifest()