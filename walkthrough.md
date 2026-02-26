# Walkthrough: BigQuery AI Data Analyst

Este projeto automatiza a análise de tabelas do BigQuery usando o Vertex AI Gemini. Ele lê o esquema e dados de exemplo para fornecer uma interpretação de negócios, rotulagem e sugestões de mesclagem.

## Arquitetura do Projeto

- `bq_service.py`: Gerencia a conexão com o BigQuery, extração de metadados e amostras de dados.
- `ai_service.py`: Interface com o Gemini 2.5 Flash para análise semântica.
- `app.py`: Servidor Flask para a interface web.
- `main.py`: Script de orquestração via terminal.

## Como Executar

### 1. Preparação da Conta de Serviço
Certifique-se de que a Conta de Serviço (o e-mail no arquivo `key.json`) tenha os seguintes papéis (roles) no Google Cloud Console:
- **BigQuery Data Viewer**: Para ler os esquemas.
- **BigQuery Job User**: Para executar as queries de amostra.
- **Vertex AI User**: Para usar o modelo Gemini.
- **Leitor (Viewer)**: Diretamente no arquivo do Google Drive (se houver tabelas externas).

### 2. Instalação e Requisitos
Garanta que todas as bibliotecas, incluindo as de performance, estejam instaladas:
```powershell
pip install -r requirements.txt
pip install google-cloud-bigquery-storage db-dtypes flask flask-cors
```

### 3. Execução (Versão Web - Recomendado)
O novo modo visual facilita muito a leitura dos relatórios:
```powershell
python app.py
```
1. No seu navegador, acesse `http://127.0.0.1:5000`.
2. Preencha o Project ID, Dataset ID e o caminho da sua chave JSON.
3. Clique em **Analisar Dataset**.
4. O relatório será exibido formatado e com design premium.

### 4. Execução (Versão Terminal)
Para uma execução rápida via linha de comando:
```powershell
python main.py
```

## Exemplo de Saída Esperada

O relatório gerado pelo AI incluirá:
- **Interpretação**: "A tabela `users` contém informações cadastrais de clientes..."
- **Dicionário de Colunas**: Explicação didática de cada campo.
- **Rótulos**: `Vendas`, `CRM`, `Geolocalização`.
- **Sugestões de Mesclagem**: "A tabela `orders` pode ser unida à `users` através da coluna `user_id` para correlacionar compras com perfis demográficos."

---
> [!IMPORTANT]
> **Tabelas no Google Drive:** Se o dataset contiver tabelas externas conectadas a arquivos no Google Drive (como planilhas), certifique-se de que o e-mail da sua Conta de Serviço (`client_email` no `key.json`) tenha permissão de **Leitor** (Viewer) no arquivo original da planilha.
