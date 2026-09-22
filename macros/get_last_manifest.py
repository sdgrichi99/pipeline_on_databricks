import os
import requests

def download_manifest():
    print("dbt Manifest Download")
    
    host = os.environ.get("DATABRICKS_HOST", "").rstrip("/")
    token = os.environ.get("DATABRICKS_TOKEN") or os.environ.get("DBT_ACCESS_TOKEN")
    
    if not host.startswith("http"):
        host = f"https://{host}"
        
    volume_path = "/Volumes/workspace_prod/default/dbt_artifacts/manifest.json"
    local_output_path = "target/manifest.json"
    
    os.makedirs("target", exist_ok=True)
    
    print(f"Sorgente Volume Databricks: {volume_path}")
    print("Download in corso...")
    
    # Chiamata REST API diretta al Files API di Databricks
    url = f"{host}/api/2.0/fs/files{volume_path}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        with open(local_output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Manifest scaricato con successo in '{local_output_path}'!")
    else:
        print(f"Errore durante il download del manifest! Status code: {response.status_code}")
        print(f"Risposta: {response.text}")
        raise RuntimeError(f"Download fallito con codice {response.status_code}")

if __name__ == "__main__":
    download_manifest()