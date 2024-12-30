@celery.task(bind=True, max_retries=3, default_retry_delay=5)
def fetch_weather_data(self, city):
    try:
        response = requests.get(
            "<api_url>",
            params={"city": city, "apikey": get_next_api_key()},
            timeout=5
        )
        response.raise_for_status()
        return parse_response(response.json())
    except requests.exceptions.RequestException as exc:
        # Retry in case of network issues, timeouts, or server errors
        raise self.retry(exc=exc)

API_KEYS = ["KEY1", "KEY2", "KEY3"]
api_key_index = 0

def get_next_api_key():
    global api_key_index
    key = API_KEYS[api_key_index]
    api_key_index = (api_key_index + 1) % len(API_KEYS)
    return key