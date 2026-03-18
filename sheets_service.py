import re
from googleapiclient.discovery import build
from google.oauth2 import service_account

class SheetsService:
    def __init__(self, service_account_info: any = None):
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.readonly"
        ]
        self.creds = None
        if service_account_info:
            if isinstance(service_account_info, dict):
                self.creds = service_account.Credentials.from_service_account_info(
                    service_account_info, scopes=self.scopes
                )
            else:
                self.creds = service_account.Credentials.from_service_account_file(
                    service_account_info, scopes=self.scopes
                )
        
        # Build the service
        self.service = build('sheets', 'v4', credentials=self.creds)

    def extract_spreadsheet_id(self, url: str):
        """Extracts the spreadsheet ID from a Google Sheets URL."""
        match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", url)
        return match.group(1) if match else None

    def get_spreadsheet_metadata(self, spreadsheet_id: str):
        """Fetches metadata and sample data from a spreadsheet."""
        try:
            spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            title = spreadsheet.get('properties', {}).get('title', 'Unknown Spreadsheet')
            sheets = spreadsheet.get('sheets', [])
            
            inventory = []
            for sheet in sheets:
                sheet_name = sheet.get('properties', {}).get('title')
                
                # Fetch first 10 rows to determine schema
                range_name = f"'{sheet_name}'!A1:Z10"
                result = self.service.spreadsheets().values().get(
                    spreadsheetId=spreadsheet_id, range=range_name).execute()
                values = result.get('values', [])
                
                if not values:
                    continue
                
                # Assume first row is header
                headers = values[0]
                sample_rows = []
                if len(values) > 1:
                    for row in values[1:6]: # Get up to 5 sample rows
                        row_dict = {}
                        for i, header in enumerate(headers):
                            if i < len(row):
                                row_dict[header] = row[i]
                        sample_rows.append(row_dict)
                
                schema = [{"name": h, "type": "string", "mode": "NULLABLE"} for h in headers]
                
                inventory.append({
                    "table_id": f"{title} - {sheet_name}",
                    "description": f"Google Sheet: {title}, Aba: {sheet_name}",
                    "num_rows": "N/A (Google Sheet)",
                    "schema": schema,
                    "sample_data": sample_rows
                })
            
            return inventory
        except Exception as e:
            print(f"Error fetching sheet metadata: {e}")
            return []

    def get_multiple_sheets_inventory(self, urls: list):
        all_inventory = []
        for url in urls:
            spreadsheet_id = self.extract_spreadsheet_id(url)
            if spreadsheet_id:
                sheet_inventory = self.get_spreadsheet_metadata(spreadsheet_id)
                all_inventory.extend(sheet_inventory)
        return all_inventory
