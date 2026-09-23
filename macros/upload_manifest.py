import os
from databricks.sdk import WorkspaceClient

DEFAULT_VOLUME = "/Volumes/workspace_prd/default/dbt_artifacts/manifest.json"

def upload_manifest():
    local_file = os.path.join("target", "manifest.json")
    volume_path = os.environ.get("DBT_MANIFEST_VOLUME_PATH", DEFAULT_VOLUME)

    print("dbt Manifest Upload")
    print(f"File locale da caricare: {local_file}")
    print(f"Destinazione Volume Databricks: {volume_path}")

    if not os.path.exists(local_file):
        raise FileNotFoundError(f"Errore: Il file {local_file} non esiste. Esegui prima 'dbt compile'.")

    host = os.environ.get("DATABRICKS_HOST", "").strip().rstrip("/")
    token = (os.environ.get("DATABRICKS_TOKEN") or os.environ.get("DBT_ACCESS_TOKEN") or "").strip()

    if not host or not token:
        raise ValueError("DATABRICKS_HOST e DATABRICKS_TOKEN devono essere definiti.")

    if not host.startswith("http://") and not host.startswith("https://"):
        host = f"https://{host}"

    print("Caricamento del file manifest tramite Databricks SDK in corso...")

    try:
        # Inizializzazione SDK con auth_type="pat" per forzare l'uso del token
        w = WorkspaceClient(host=host, token=token, auth_type="pat")
        
        with open(local_file, "rb") as f:
            w.files.upload(volume_path, f, overwrite=True)
            
        print("Manifest aggiornato e caricato con successo sul Volume Databricks!")

    except Exception as e:
        print(f"Errore critico durante l'upload del manifest: {str(e)}")
        raise e

if __name__ == "__main__":
    upload_manifest()