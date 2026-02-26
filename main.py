import sys
from bq_service import BigQueryService
from ai_service import AIService

def main():
    print("=== BigQuery AI Data Analyst ===")
    
    project_id = input("Enter your Google Cloud Project ID: ").strip()
    dataset_id = input("Enter the BigQuery Dataset ID: ").strip()
    location = input("Enter Gemini Location (default: us-central1): ").strip() or "us-central1"
    sa_path = input("Enter path to Service Account JSON (leave empty to use default): ").strip() or None
    
    if not project_id or not dataset_id:
        print("Error: Project ID and Dataset ID are required.")
        sys.exit(1)

    try:
        print(f"\n1. Fetching metadata for dataset: {dataset_id}...")
        bq = BigQueryService(project_id, service_account_path=sa_path)
        inventory = bq.get_dataset_inventory(dataset_id)
        
        if not inventory:
            print("No tables found in the specified dataset.")
            return

        print(f"   Found {len(inventory)} tables. Sending to AI for analysis...")

        print("\n2. Analyzing data with Vertex AI Gemini...")
        ai = AIService(project_id, location=location, service_account_path=sa_path)
        analysis_report = ai.analyze_tables(inventory)

        print("\n=== AI ANALYSIS REPORT ===")
        print(analysis_report)
        print("\n==========================")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
