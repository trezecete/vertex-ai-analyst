# BigQuery AI Data Analyst & Labeler 🚀

Este projeto utiliza o **Vertex AI Gemini 2.5 Flash** para analisar e interpretar tabelas do BigQuery de forma didática e visual.

## Funcionalidades
- **Análise Semântica**: Explicação do que cada tabela representa em termos de negócio.
- **Dicionário de Dados**: Explicação detalhada de cada coluna.
- **Sugestão de Mesclagem**: Identificação de tabelas relacionadas.
- **Diagrama Visual**: Geração de diagrama de relacionamento usando Mermaid.js.
- **Interface Web**: Dashboard moderno com efeito glassmorphism.

## Como Usar

### 1. Configuração do Google Cloud
- Crie uma **Conta de Serviço** no Google Cloud Console.
- Adicione as permissões: `BigQuery Data Viewer`, `BigQuery Job User` e `Vertex AI User`.
- Baixe a chave JSON da conta de serviço.

### 2. Instalação
```bash
pip install -r requirements.txt
pip install google-cloud-bigquery-storage db-dtypes flask flask-cors
```

### 3. Execução
```bash
python app.py
```
Acesse `http://127.0.0.1:5000`. 

O sistema tentará usar automaticamente o arquivo `key/key.json` se ele existir na pasta do projeto. Caso contrário, você pode carregar uma chave JSON personalizada clicando no botão **"Carregar arquivo JSON de serviço personalizado"**.

## Documentação Detalhada
Para um passo a passo completo sobre permissões, instalação e fluxo de uso, consulte o arquivo [walkthrough.md](./walkthrough.md).

## Segurança
⚠️ **IMPORTANTE**: Nunca suba o arquivo `key.json` para o GitHub. Este projeto já inclui um `.gitignore` que protege este arquivo.
