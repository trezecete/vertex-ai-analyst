from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from bq_service import BigQueryService
from ai_service import AIService
import os

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    project_id = data.get('project_id')
    dataset_id = data.get('dataset_id')
    location = data.get('location', 'us-central1')
    sa_path = data.get('sa_path')

    if not project_id or not dataset_id:
        return jsonify({"error": "Project ID and Dataset ID are required."}), 400

    try:
        # 1. Fetch metadata
        bq = BigQueryService(project_id, service_account_path=sa_path)
        inventory = bq.get_dataset_inventory(dataset_id)
        
        if not inventory:
            return jsonify({"error": "No tables found in the specified dataset."}), 404

        # 2. Analyze with AI
        ai = AIService(project_id, location=location, service_account_path=sa_path)
        analysis_report = ai.analyze_tables(inventory)

        return jsonify({
            "report": analysis_report,
            "table_count": len(inventory)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
