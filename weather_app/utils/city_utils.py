import re

CITY_REGEX = re.compile(r'^[a-zA-Z\u0400-\u04FF\s\'-]+$')  # Example

def normalize_city_name(raw_name):
    # Basic check
    if not CITY_REGEX.match(raw_name):
        return ""
    
    # Example corrections
    lowered = raw_name.lower()
    if lowered == "londn":
        return "London"
    if lowered in ["киев", "kyiv"]:
        return "Kyiv"
    # ... Add more known corrections ...

    return raw_name.title()  # or some transliteration logic

CITY_REGION_MAP = {
    "kyiv": "Europe",
    "london": "Europe",
    "paris": "Europe",
    "new york": "America",
    # ...
}

def map_to_region(city_name):
    # Normalize to lower for lookup
    return CITY_REGION_MAP.get(city_name.lower(), "Other")