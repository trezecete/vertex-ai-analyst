from sheets_service import SheetsService
import os
import json

def test_sheets():
    # Use key/key.json if available
    creds = None
    if os.path.exists('key/key.json'):
        creds = 'key/key.json'
        print("Using key/key.json for credentials.")
    else:
        print("No credentials found. This test might fail if the sheet is private.")

    sheets = SheetsService(service_account_info=creds)
    
    # Example public/sample sheet URL
    # This is a sample sheet from Google
    url = "https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit"
    
    print(f"Extracting ID from: {url}")
    sheet_id = sheets.extract_spreadsheet_id(url)
    print(f"Spreadsheet ID: {sheet_id}")
    
    if sheet_id:
        print("Fetching metadata...")
        inventory = sheets.get_spreadsheet_metadata(sheet_id)
        print(f"Found {len(inventory)} sheets/tabs.")
        for item in inventory:
            print(f"- Sheet: {item['table_id']}")
            print(f"  Columns: {len(item['schema'])}")
            print(f"  Sample rows: {len(item['sample_data'])}")
            if item['sample_data']:
                print(f"  First sample row: {item['sample_data'][0]}")

if __name__ == "__main__":
    test_sheets()
