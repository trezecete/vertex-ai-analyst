from google.cloud import aiplatform
import google.auth
from google.oauth2 import service_account
import sys

def list_endpoint_models(project_id, location, service_account_path=None):
    print(f"\n--- Checking Vertex AI Models in {location} ---")
    try:
        if service_account_path:
            credentials = service_account.Credentials.from_service_account_file(service_account_path)
            aiplatform.init(project=project_id, location=location, credentials=credentials)
        else:
            aiplatform.init(project=project_id, location=location)

        # We use Model.list() to see what models are available in the registry
        print("Fetching models from registry...")
        models = aiplatform.Model.list()
        
        if not models:
            print(f"No models found in region {location}. This might mean the API is disabled or no models are enabled for this project/region.")
        else:
            print(f"Found {len(models)} models:")
            for model in models:
                print(f" - {model.display_name} (ID: {model.name})")

    except Exception as e:
        print(f"Error checking models: {e}")

if __name__ == "__main__":
    p_id = input("Project ID: ").strip()
    loc = input("Location (default us-central1): ").strip() or "us-central1"
    key = input("Path to key.json (optional): ").strip() or None
    list_endpoint_models(p_id, loc, key)
