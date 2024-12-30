from flask import Flask
from celery_app import make_celery
from flask import request, jsonify
from tasks import process_weather_data
from utils.city_utils import normalize_city_name
from celery.result import AsyncResult
import os, json


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'

celery = make_celery(app)

@app.route('/weather', methods=['POST'])
def create_weather_task():
    data = request.get_json(force=True)
    
    # Validate input
    if 'cities' not in data or not isinstance(data['cities'], list):
        return jsonify({"error": "Invalid input. Expected 'cities' as a list."}), 400

    cleaned_cities = []
    for city in data['cities']:
        normalized = normalize_city_name(city)  # e.g., fix typos, transliterate
        if normalized:  # if empty or invalid, we might skip or log
            cleaned_cities.append(normalized)

    # Start asynchronous task
    task = process_weather_data.delay(cleaned_cities)

    return jsonify({"task_id": task.id}), 202

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task_result = AsyncResult(task_id, app=celery)

    if task_result.state == 'PENDING':
        return jsonify({"status": "running"}), 200
    elif task_result.state == 'FAILURE':
        return jsonify({"status": "failed", "error": str(task_result.result)}), 200
    elif task_result.state == 'SUCCESS':
        return jsonify({"status": "completed", "results_url": "/results"}), 200
    else:
        # other states: STARTED, RETRY, etc.
        return jsonify({"status": task_result.state.lower()}), 200

@app.route('/results/<region>', methods=['GET'])
def get_results(region):
    folder_path = os.path.join('weather_data', region)
    if not os.path.exists(folder_path):
        return jsonify({"error": "Region not found"}), 404
    
    all_data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as f:
                content = json.load(f)
                all_data.extend(content)
    
    return jsonify({"region": region, "data": all_data}), 200