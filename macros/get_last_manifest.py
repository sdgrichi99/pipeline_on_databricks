import os
from databricks.sdk import WorkspaceClient

def download_manifest():
    print("dbt Manifest Download")
    
    host = os.environ.get("DATABRICKS_HOST", "").strip().rstrip("/")
    token = os.environ.get("DATABRICKS_TOKEN", "").strip()
    
    if not host or not token:
        raise ValueError("DATABRICKS_HOST e DATABRICKS_TOKEN devono essere definiti.")

    if not host.startswith("http://") and not host.startswith("https://"):
        host = f"https://{host}"

    volume_path = "/Volumes/workspace_prd/default/dbt_artifacts/manifest.json"
    
    # SEPARAZIONE: Salviamo in una cartella dedicata
    local_dir = "target_remote"
    local_output_path = os.path.join(local_dir, "manifest.json")
    os.makedirs(local_dir, exist_ok=True)

    print(f"Host: {host}")
    print(f"Sorgente Volume: {volume_path}")
    print(f"Destinazione Locale: {local_output_path}")
    print("Download in corso tramite Databricks SDK...")

    try:
        w = WorkspaceClient(host=host, token=token, auth_type="pat")
        
        response = w.files.download(volume_path)
        with open(local_output_path, "wb") as f:
            f.write(response.contents.read())
            
        print(f"Manifest scaricato con successo in '{local_output_path}'!")

    except Exception as e:
        print(f"Errore critico durante il download del manifest: {str(e)}")
        raise e

if __name__ == "__main__":
    download_manifest()