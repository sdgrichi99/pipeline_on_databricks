import os
import shutil
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound

DEFAULT_VOLUME = "/Volumes/workspace_prod/default/dbt_artifacts/manifest.json"

def download_manifest():
    local_dir = "state"
    local_file = os.path.join(local_dir, "manifest.json")
    volume_path = os.environ.get("DBT_MANIFEST_VOLUME_PATH", DEFAULT_VOLUME)

    print("=== dbt Manifest Downloader ===")
    print(f"Sorgente Volume Databricks: {volume_path}")
    os.makedirs(local_dir, exist_ok=True)

    # Recupero credenziali con fallback su DBT_ACCESS_TOKEN
    host = os.environ.get("DATABRICKS_HOST")
    token = os.environ.get("DATABRICKS_TOKEN") or os.environ.get("DBT_ACCESS_TOKEN")

    try:
        # Inizializziamo il client passando esplicitamente le credenziali se presenti
        if host and token:
            w = WorkspaceClient(host=host, token=token)
        else:
            w = WorkspaceClient()

        print("Download in corso...")
        response = w.files.download(volume_path)
        with open(local_file, "wb") as f:
            shutil.copyfileobj(response.contents, f)
        print(f"Manifest scaricato in: {local_file}")

    # Se il manifest non viene trovato nel volume, continua per consentire la Full Build
    except NotFound:
        print("AVVISO: Nessun manifest trovato sul Volume Databricks (Primo avvio!).")
        print("La pipeline continuerà senza confronto dello stato (Full Build).")
    
    # Errore se abbiamo un problema di configurazione/autenticazione
    except Exception as e:
        print(f"Errore critico inaspettato durante il download: {str(e)}")
        raise e

if __name__ == "__main__":
    download_manifest()