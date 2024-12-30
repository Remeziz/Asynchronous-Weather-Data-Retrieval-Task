def is_valid_weather_data(data):
    # Check for temperature key
    temperature = data.get("temperature")
    if temperature is None:
        return False
    # Check range
    if temperature < -50 or temperature > 50:
        return False
    
    # Check for description
    if "description" not in data:
        return False
    
    return True