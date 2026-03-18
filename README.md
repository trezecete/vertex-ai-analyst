# BigQuery & Sheets AI Data Analyst 🚀

Este projeto utiliza o **Vertex AI Gemini 1.5 Flash (ou superior)** para analisar e interpretar dados de tabelas do **BigQuery** e planilhas do **Google Sheets** de forma didática e visual.

## 🌟 Funcionalidades

- **Análise Semântica Multicloud**: Explicação didática do que os dados representam para o negócio, suportando BigQuery e Google Sheets.
- **Dicionário de Dados Automatizado**: Explicação exata do significado de cada coluna e sugestão de categorias.
- **Sugestão de Relacionamentos**: Identificação inteligente de chaves de ligação (`JOINs`) e ideias analíticas de cruzamento.
- **Dashboards Dinâmicos**: Criação instantânea de visualizações usando **Chart.js**, com filtros em tempo real e descrições de insights por gráfico.
- **Persistência e Reuso**: Salve a configuração do seu dashboard em JSON e recarregue-o futuramente sem gastar novos créditos de IA.
- **Dados em Tempo Real**: Botão para atualizar capturar os números mais recentes da fonte (Sheets/BQ) diretamente no dashboard.
- **Exportação DOCX**: Baixe o relatório completo de análise em formato Word para compartilhamento.

## 🛠️ Como Usar

### 1. Configuração do Google Cloud
- Crie uma **Conta de Serviço** no Google Cloud Console.
- Ative as APIs: `BigQuery API`, `Google Sheets API` e `Vertex AI API`.
- Adicione as permissões: `BigQuery Data Viewer`, `BigQuery Job User`, `Sheets Viewer` e `Vertex AI User`.
- Baixe a chave JSON e armazene na pasta `key/key.json` (protegida pelo `.gitignore`).

### 2. Instalação
```bash
pip install -r requirements.txt
```

### 3. Execução
```bash
python app.py
```
Acesse `http://127.0.0.1:5000` no seu navegador.

## 📁 Estrutura do Projeto

- `app.py`: Servidor principal e API Flask.
- `ai_service.py`: Lógica de integração com Gemini.
- `bq_service.py`: Interface com BigQuery.
- `sheets_service.py`: Interface com Google Sheets.
- `static/`: Frontend (HTML/CSS/JS) com design moderno.
- `scripts/`: Utilitários de teste e verificação.
- `main.py`: Versão CLI do analista para terminal.

## ⚠️ Segurança
Este projeto foi configurado para **NUNCA** subir arquivos JSON de credenciais para o GitHub. Mantenha suas chaves sempre na pasta `key/` ou carregue-as dinamicamente pela interface.

---
*Desenvolvido para transformar dados técnicos em decisões de negócio.*
