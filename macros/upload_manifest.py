import os
import requests

DEFAULT_VOLUME = "/Volumes/workspace_prod/default/dbt_artifacts/manifest.json"

def upload_manifest():
    local_file = os.path.join("target", "manifest.json")
    volume_path = os.environ.get("DBT_MANIFEST_VOLUME_PATH", DEFAULT_VOLUME)

    print("dbt Manifest Upload")
    print(f"File locale da caricare: {local_file}")
    print(f"Destinazione Volume Databricks: {volume_path}")

    if not os.path.exists(local_file):
        raise FileNotFoundError(
            f"Errore: Il file {local_file} non esiste. Assicurati che 'dbt compile' sia stato eseguito con successo."
        )

    host = os.environ.get("DATABRICKS_HOST", "").rstrip("/")
    token = os.environ.get("DATABRICKS_TOKEN") or os.environ.get("DBT_ACCESS_TOKEN")

    if not host or not token:
        raise ValueError("DATABRICKS_HOST e DATABRICKS_TOKEN (o DBT_ACCESS_TOKEN) devono essere definiti.")

    if not host.startswith("http"):
        host = f"https://{host}"

    print("Caricamento del file manifest su Databricks Volume in corso...")

    # Chiamata REST API diretta per l'upload sul Volume (overwrite=true)
    url = f"{host}/api/2.0/fs/files{volume_path}?overwrite=true"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream"
    }

    try:
        with open(local_file, "rb") as f:
            response = requests.put(url, headers=headers, data=f)

        if response.status_code in [200, 201]:
            print("✅ Manifest aggiornato e caricato con successo sul Volume Databricks!")
        else:
            print(f"Errore durante l'upload del manifest! Status code: {response.status_code}")
            print(f"Risposta: {response.text}")
            raise RuntimeError(f"Upload fallito con codice {response.status_code}")

    except Exception as e:
        print(f"Errore critico durante l'upload del manifest: {str(e)}")
        raise e

if __name__ == "__main__":
    upload_manifest()