import vertexai
from vertexai.generative_models import GenerativeModel, Part
import json

class AIService:
    def __init__(self, project_id: str, location: str = "us-central1", service_account_info: any = None):
        if service_account_info:
            import google.auth
            from google.oauth2 import service_account
            if isinstance(service_account_info, dict):
                credentials = service_account.Credentials.from_service_account_info(service_account_info)
            else:
                credentials = service_account.Credentials.from_service_account_file(service_account_info)
            vertexai.init(project=project_id, location=location, credentials=credentials)
        else:
            vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel("gemini-2.5-flash")

    def analyze_tables(self, inventory: list):
        prompt = f"""
        Você é um consultor de dados sênior e um excelente professor. Sua tarefa é analisar os metadados das tabelas do BigQuery ou abas do Google Sheets fornecidos e criar um relatório de metadados EXTREMAMENTE DIDÁTICO e PROFISSIONAL em PORTUGUÊS (Brasil).

        ESTRUTURA DO RELATÓRIO (SIGA RIGOROSAMENTE):

        1. **Resumo da Fonte de Dados**: 
           - Identifique se é um Banco de Dados (BigQuery) ou uma Planilha (Google Sheets).
           - Forneça uma **descrição da planilha/dataset como um todo**, explicando seu propósito geral no negócio.

        2. **Análise por Aba/Tabela**:
           Para CADA aba (se for planilha) ou tabela (se for BigQuery), crie uma seção contendo:
           - **Descrição da Aba/Tabela**: Explique o que esses dados representam especificamente.
           - **Dicionário de Dados**: Apresente uma tabela ou lista clara com:
             - Nome da Coluna
             - Significado para o Negócio (descrição didática)
             - Exemplo de Dado (baseado na amostra fornecida)
           - **Relacionamentos Internos**: Identifique como esta aba se relaciona com OUTRAS ABAS DA MESMA PLANILHA (ou outras tabelas do mesmo dataset). Explique qual campo é a chave de ligação.

        3. **Relacionamentos entre Fontes Distintas** (Caso haja mais de uma planilha/dataset):
           - Faça uma descrição detalhada de como as diferentes planilhas ou datasets se conectam entre si para formar uma visão 360º do negócio.

        4. **Sugestões de Business Intelligence (KPIs e Dashboards)**:
           - **KPIs Sugeridos**: Com base nos campos identificados, sugira indicadores-chave de desempenho.
           - **Gráficos e Visualizações**: Sugira o MÁXIMO de visões gráficas possíveis (Barras, Linhas, Pizza, Heatmap, etc.) e explique POR QUE cada uma agrega valor.
           - **Proposta de Dashboard**: Descreva como seria um dashboard ideal consolidando essas fontes.

        REGRAS DE ESTILO:
        - Use Markdown elegante.
        - Use emojis para facilitar a leitura.
        - O público-alvo são gestores e analistas de negócio, não técnicos. Use linguagem clara e acessível.
        - Se houver nomes de colunas técnicos ou siglas (ex: 'id_cli', 'vnd_mt'), traduza para o termo de negócio correto (ex: 'Código do Cliente', 'Montante de Venda').

        Metadados e Amostras para Análise:
        {json.dumps(inventory, indent=2, default=str)}

        Responda em um estilo Markdown elegante, pronto para ser exibido em uma interface web premium, usando emojis e divisões claras.
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def generate_dashboard_config(self, inventory):
        """Gera uma configuração JSON para um dashboard dinâmico."""
        prompt = f"""
        Com base nos metadados e amostras de dados fornecidos abaixo, crie uma configuração JSON para um dashboard dinâmico.
        O objetivo é visualizar os insights mais importantes e permitir que os dados sejam atualizados futuramente.

        REGRAS:
        1. Retorne APENAS o JSON, sem markdown ou explicações.
        2. A estrutura deve ser:
           {{
             "title": "Título do Dashboard",
             "charts": [
               {{
                 "id": "chart1",
                 "type": "bar|line|pie|doughnut",
                 "title": "Título do Gráfico",
                 "description": "Explicação do que este gráfico analisa e qual o insight esperado.",
                 "label_field": "nome_da_coluna_para_labels",
                 "value_field": "nome_da_coluna_para_valores",
                 "table_id": "id_da_tabela_ou_aba",
                 "data": {{
                   "labels": ["Label 1", "Label 2", ...],
                   "datasets": [{{
                     "label": "Nome da Métrica",
                     "data": [10, 20, ...]
                   }}]
                 }}
               }}
             ]
           }}
        3. Use os dados de 'sample_data' para preencher os valores iniciais.
        4. 'label_field' e 'value_field' DEVEM ser os nomes exatos das colunas encontradas no schema/sample_data.
        5. 'table_id' deve ser o campo 'table_id' do inventário correspondente aos dados.
        6. 'description' deve ser uma frase curta e didática que agregue valor ao usuário de negócio.

        Metadados:
        {json.dumps(inventory, indent=2, default=str)}
        """
        
        response = self.model.generate_content(prompt)
        # Limpar possíveis markdown wrappers para extrair o JSON puro
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:-3].strip()
        elif text.startswith('```'):
            text = text[3:-3].strip()
            
        try:
            return json.loads(text)
        except:
            return {"error": "Falha ao gerar JSON", "raw": text}

    def suggest_merges_only(self, inventory: list):
        prompt = f"""
        Analyze these BigQuery tables and suggest specific SQL merge/join operations that would be beneficial for data Consolidation.
        Explain the reasoning for each suggestion (e.g., matching 'user_id', complementary descriptive fields).

        Tables:
        {json.dumps(inventory, indent=2, default=str)}
        """
        response = self.model.generate_content(prompt)
        return response.text
