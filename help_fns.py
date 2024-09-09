import json

from datetime import datetime

def get_current_datetime() -> str:
    """Returns the current date and time in the format: 'MM/DD/YYYY, HH:MM AM/PM'."""
    now = datetime.now()
    formatted_datetime = now.strftime("%m/%d/%Y, %I:%M %p")
    return formatted_datetime

def extract_weather_info(json_data, units='default'):
    # Extract coordinates
    lon = json_data.get('coord', {}).get('lon', 'N/A')
    lat = json_data.get('coord', {}).get('lat', 'N/A')

    # Extract weather description
    weather_main = json_data.get('weather', [{}])[0].get('main', 'N/A')
    weather_description = json_data.get('weather', [{}])[0].get('description', 'N/A')

    # Extract temperature and attach appropriate units
    if units == 'metric':
        temp_unit = '°C'
        wind_speed_unit = 'm/s'
    elif units == 'imperial':
        temp_unit = '°F'
        wind_speed_unit = 'mph'
    else:
        temp_unit = 'K'
        wind_speed_unit = 'm/s'

    temp = json_data.get('main', {}).get('temp', 'N/A')
    feels_like = json_data.get('main', {}).get('feels_like', 'N/A')
    temp_min = json_data.get('main', {}).get('temp_min', 'N/A')
    temp_max = json_data.get('main', {}).get('temp_max', 'N/A')
    pressure = json_data.get('main', {}).get('pressure', 'N/A')
    humidity = json_data.get('main', {}).get('humidity', 'N/A')
    sea_level = json_data.get('main', {}).get('sea_level', 'N/A')
    grnd_level = json_data.get('main', {}).get('grnd_level', 'N/A')

    # Extract visibility
    visibility = json_data.get('visibility', 'N/A')

    # Extract wind information
    wind_speed = json_data.get('wind', {}).get('speed', 'N/A')
    wind_deg = json_data.get('wind', {}).get('deg', 'N/A')
    wind_gust = json_data.get('wind', {}).get('gust', 'N/A')

    # Extract rain information
    rain_1h = json_data.get('rain', {}).get('1h', 'N/A')

    # Extract cloudiness
    cloudiness = json_data.get('clouds', {}).get('all', 'N/A')

    # Extract system information
    country = json_data.get('sys', {}).get('country', 'N/A')
    sunrise = convert_unix_timestamp(json_data.get('sys', {}).get('sunrise', 'N/A'))
    sunset = convert_unix_timestamp(json_data.get('sys', {}).get('sunset', 'N/A'))

    # Extract city and timezone information
    city_name = json_data.get('name', 'N/A')
    timezone = json_data.get('timezone', 'N/A')

    # Format output
    weather_info = {
        "Coordinates": f"Longitude: {lon}, Latitude: {lat}",
        "Weather": f"{weather_main} ({weather_description})",
        "Temperature": f"{temp} {temp_unit}",
        "Feels Like": f"{feels_like} {temp_unit}",
        "Minimum Temperature": f"{temp_min} {temp_unit}",
        "Maximum Temperature": f"{temp_max} {temp_unit}",
        "Pressure": f"{pressure} hPa",
        "Humidity": f"{humidity}%",
        "Sea Level Pressure": f"{sea_level} hPa",
        "Ground Level Pressure": f"{grnd_level} hPa",
        "Visibility": f"{visibility} meters",
        "Wind Speed": f"{wind_speed} {wind_speed_unit}",
        "Wind Direction": f"{wind_deg}°",
        "Wind Gust": f"{wind_gust} {wind_speed_unit}",
        "Rain Volume (Last 1 hour)": f"{rain_1h} mm",
        "Cloudiness": f"{cloudiness}%",
        "Country": country,
        "Sunrise": sunrise,
        "Sunset": sunset,
        "City Name": city_name,
        "Timezone": timezone
    }

    return weather_info

def convert_unix_timestamp(unix_timestamp):
    # Convert Unix timestamp to datetime object
    dt = datetime.fromtimestamp(unix_timestamp)
    
    # Format the datetime object to the desired format
    formatted_time = dt.strftime("%I:%M %p, %m/%d/%Y")
    
    return formatted_time



def process_weather_data(json_data, units="metric"):
    # Define unit conversions based on input units
    if units == "metric":
        temp_unit = "°C"
        wind_speed_unit = "m/s"
    elif units == "imperial":
        temp_unit = "°F"
        wind_speed_unit = "mph"
    else:  # Default (Kelvin and m/s)
        temp_unit = "K"
        wind_speed_unit = "m/s"
    
    # Extract city and general information
    city_name = json_data.get("city", {}).get("name", "N/A")
    country = json_data.get("city", {}).get("country", "N/A")
    
    # Weather forecast list
    weather_list = json_data.get("list", [])
    forecast = []

    for weather in weather_list:
        # Extract datetime and convert Unix timestamp to readable format
        dt = weather.get("dt", 0)
        dt_txt = datetime.utcfromtimestamp(dt).strftime("%I:%M %p, %m/%d/%Y")

        # Extract main weather information
        temp = weather.get("main", {}).get("temp", "N/A")
        feels_like = weather.get("main", {}).get("feels_like", "N/A")
        temp_min = weather.get("main", {}).get("temp_min", "N/A")
        temp_max = weather.get("main", {}).get("temp_max", "N/A")
        pressure = weather.get("main", {}).get("pressure", "N/A")
        humidity = weather.get("main", {}).get("humidity", "N/A")

        # Extract wind information
        wind_speed = weather.get("wind", {}).get("speed", "N/A")
        wind_deg = weather.get("wind", {}).get("deg", "N/A")
        wind_gust = weather.get("wind", {}).get("gust", "N/A")

        # Extract weather description
        weather_description = weather.get("weather", [{}])[0].get("description", "N/A")

        # Format the forecast entry
        forecast_entry = {
            "City": city_name,
            "Country": country,
            "Date/Time": dt_txt,
            "Temperature": f"{temp} {temp_unit}",
            "Feels Like": f"{feels_like} {temp_unit}",
            "Min Temperature": f"{temp_min} {temp_unit}",
            "Max Temperature": f"{temp_max} {temp_unit}",
            "Pressure": f"{pressure} hPa",
            "Humidity": f"{humidity}%",
            "Wind Speed": f"{wind_speed} {wind_speed_unit}",
            "Wind Direction": f"{wind_deg}°",
            "Wind Gust": f"{wind_gust} {wind_speed_unit}",
            "Weather Description": weather_description
        }

        forecast.append(forecast_entry)
    
    return forecast



