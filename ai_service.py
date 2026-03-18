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
        Você é um consultor de dados sênior e um excelente professor. Sua tarefa é analisar os metadados das tabelas do BigQuery ou abas do Google Sheets abaixo e criar um relatório didático em PORTUGUÊS (Brasil).
        
        O público-alvo NÃO são engenheiros de dados, mas sim profissionais de negócios que precisam entender o que os dados representam e como podem ser usados.

        Para cada tabela, forneça:
        1. **O que é esta tabela?**: Explique de forma simples o conceito de negócio por trás dela. Evite termos técnicos como 'float64' ou 'string'; use 'valores monetários', 'nomes', 'datas', etc.
        2. **Dicionário de Colunas**: Liste cada coluna da tabela e explique seu significado para o negócio de forma muito didática. Se houver códigos ou siglas, tente interpretar o que significam com base nos dados.
        3. **Rótulo Sugerido**: Dê uma categoria amigável (ex: "Vendas", "Cadastro de Clientes").
        4. **Sugestões de Relacionamento**: Identifique tabelas/abas que podem ser conectadas. 
           - **Relacionamento Direto (JOIN)**: Use esta categoria para conexões óbvias e técnicas (ex: 'user_id' em ambas as tabelas). Explique qual campo é a chave de ligação.
           - **Ideia de Conexão**: Use esta categoria para sugestões analíticas ou de negócio que não possuem uma chave técnica direta óbvia, mas que fazem sentido para correlação (ex: "Podemos cruzar os dados de vendas por região com os dados de clima para ver se dias chuvosos afetam as vendas").
           - **IMPORTANTE**: Deixe bem evidente se a conexão é técnica/direta ou apenas uma ideia de análise.
        5. **Sugestões de Visualização (Gráficos/Dashboards)**: Com base nos dados, sugira o MÁXIMO de visões gráficas possíveis que agreguem valor ao negócio. 
           - Explique QUAL gráfico usar (ex: Bar, Line, Pie, Heatmap, Scatter) e POR QUE ele é útil para entender aquela métrica específica.
           - Sugira KPIs (Indicadores Chave de Desempenho) que poderiam ser criados a partir dessas tabelas.

        Metadados:
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
