from app import celery
from utils.api_handlers import fetch_weather_data
from utils.validation import is_valid_weather_data
from utils.city_utils import map_to_region
import json, os

@celery.task(bind=True)
def process_weather_data(self, cleaned_cities):
    results_by_region = {}

    for city in cleaned_cities:
        try:
            weather_response = fetch_weather_data(city)
        except Exception as e:
            # Log the error
            print(f"Error fetching data for {city}: {e}")
            continue

        # Validate data (temp range, missing fields, etc.)
        if not is_valid_weather_data(weather_response):
            print(f"Invalid data for {city}: {weather_response}")
            continue

        # Organize structured data
        city_data = {
            "city": city,
            "temperature": weather_response.get("temperature"),
            "description": weather_response.get("description")
        }

        # Classify city by region
        region = map_to_region(city)

        # Store results by region
        if region not in results_by_region:
            results_by_region[region] = []
        results_by_region[region].append(city_data)

    # Save results to JSON
    for region, data_list in results_by_region.items():
        folder_path = os.path.join('weather_data', region)
        os.makedirs(folder_path, exist_ok=True)

        file_name = f"task_{self.request.id}.json"
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)

    return {"status": "completed"}
