from google.cloud import bigquery
import pandas as pd

class BigQueryService:
    def __init__(self, project_id: str, service_account_path: str = None):
        scopes = [
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/bigquery"
        ]
        if service_account_path:
            from google.oauth2 import service_account
            credentials = service_account.Credentials.from_service_account_file(
                service_account_path, scopes=scopes
            )
            self.client = bigquery.Client(credentials=credentials, project=project_id)
        else:
            self.client = bigquery.Client(project=project_id)

    def list_datasets(self):
        return list(self.client.list_datasets())

    def list_tables(self, dataset_id: str):
        dataset_ref = self.client.dataset(dataset_id)
        return list(self.client.list_tables(dataset_ref))

    def get_table_metadata(self, dataset_id: str, table_id: str):
        table_ref = self.client.dataset(dataset_id).table(table_id)
        table = self.client.get_table(table_ref)
        
        # Get schema as a list of dicts
        schema = [{"name": field.name, "type": field.field_type, "mode": field.mode, "description": field.description} 
                  for field in table.schema]
        
        # Get sample data (first 5 rows)
        query = f"SELECT * FROM `{table.project}.{dataset_id}.{table_id}` LIMIT 5"
        sample_data = []
        try:
            sample_df = self.client.query(query).to_dataframe()
            sample_data = sample_df.to_dict(orient="records")
        except Exception as e:
            error_msg = str(e)
            if "Permission denied while getting Drive credentials" in error_msg:
                print(f"   [AVISO] Sem permissão para ler dados da tabela '{table_id}' (Tabela externa no Drive).")
                print(f"           Certifique-se de que a conta de serviço tem acesso ao arquivo.")
            else:
                print(f"   [AVISO] Erro ao buscar amostra para '{table_id}': {e}")
        
        return {
            "table_id": table_id,
            "description": table.description,
            "num_rows": table.num_rows,
            "schema": schema,
            "sample_data": sample_data
        }

    def get_dataset_inventory(self, dataset_id: str):
        tables = self.list_tables(dataset_id)
        inventory = []
        for table in tables:
            meta = self.get_table_metadata(dataset_id, table.table_id)
            inventory.append(meta)
        return inventory
