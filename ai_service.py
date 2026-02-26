import vertexai
from vertexai.generative_models import GenerativeModel, Part
import json

class AIService:
    def __init__(self, project_id: str, location: str = "us-central1", service_account_path: str = None):
        if service_account_path:
            import google.auth
            from google.oauth2 import service_account
            credentials = service_account.Credentials.from_service_account_file(service_account_path)
            vertexai.init(project=project_id, location=location, credentials=credentials)
        else:
            vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel("gemini-2.5-flash")

    def analyze_tables(self, inventory: list):
        prompt = f"""
        Você é um consultor de dados sênior e um excelente professor. Sua tarefa é analisar os metadados das tabelas do BigQuery abaixo e criar um relatório didático em PORTUGUÊS (Brasil).
        
        O público-alvo NÃO são engenheiros de dados, mas sim profissionais de negócios que precisam entender o que os dados representam e como podem ser usados.

        Para cada tabela, forneça:
        1. **O que é esta tabela?**: Explique de forma simples o conceito de negócio por trás dela. Evite termos técnicos como 'float64' ou 'string'; use 'valores monetários', 'nomes', 'datas', etc.
        2. **Dicionário de Colunas**: Liste cada coluna da tabela e explique seu significado para o negócio de forma muito didática. Se houver códigos ou siglas, tente interpretar o que significam com base nos dados.
        3. **Rótulo Sugerido**: Dê uma categoria amigável (ex: "Vendas", "Cadastro de Clientes").
        4. **Sugestão de Conexão (Merge)**: Identifique tabelas que "conversam" entre si. Explique POR QUE elas devem ser conectadas (ex: "Você pode juntar esta tabela de pedidos com a de clientes para saber quem comprou o quê").
        5. **Diagrama de Relacionamento (Mermaid)**: Ao final do relatório, gere um bloco de código `mermaid` com um `erDiagram`. 
           - IMPORTANTE: No `erDiagram`, use o formato `TABELA1 ||--o{{ TABELA2 : "relacao" }}`.
           - Não use caracteres especiais ou espaços nos nomes das tabelas.
           - Certifique-se de que cada relação tenha um texto descritivo entre aspas.
           - Se não houver conexões claras, crie apenas os blocos das tabelas sem linhas de ligação.

        Metadados das Tabelas:
        {json.dumps(inventory, indent=2, default=str)}

        Responda em um estilo Markdown elegante, pronto para ser exibido em uma interface web premium, usando emojis e divisões claras.
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def suggest_merges_only(self, inventory: list):
        prompt = f"""
        Analyze these BigQuery tables and suggest specific SQL merge/join operations that would be beneficial for data Consolidation.
        Explain the reasoning for each suggestion (e.g., matching 'user_id', complementary descriptive fields).

        Tables:
        {json.dumps(inventory, indent=2, default=str)}
        """
        response = self.model.generate_content(prompt)
        return response.text
