import pandas as pd
from llama_index.experimental.query_engine.pandas import PandasQueryEngine
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from creds import weather_key,csv_file,OPENAI_API_KEY
import json
import requests
from help_fns import extract_weather_info, process_weather_data,get_current_datetime
import openai
import numpy as np
# Initialize the OpenAI API key
openai.api_key = OPENAI_API_KEY


def reverse_geocoding(lat: float, lon: float) -> str:
    """Returns the closest one city to the lattitude and longitude and the city's name"""
    url =f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&appid={weather_key}"
    response = requests.get(url)

    # Check if the request was successful
    add_st=""
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        name_value_pairs = [(entry['name'], entry['lat'], entry['lon']) for entry in data]

        for name, lat, lon in name_value_pairs:
            add_st+=f"City Name: {name}, Latitude: {lat}, Longitude: {lon}"
           # print(f"Name: {name}, Latitude: {lat}, Longitude: {lon}")
        # Print the data (customize this part based on what you need)
       # print(json.dumps(data,indent=4))
    else:
        print(f"Failed to retrieve data: HTTP {response.status_code}")
    
    # Display the results
    
    #print("here",add_st)
    return add_st

reverse_geocoding_tool = FunctionTool.from_defaults(fn=reverse_geocoding)

def geocoding(city_name:str) -> str:
    """returns the lattitude, longitude, State, and country of origin of all cities sharing the name passed"""
    
    n=10
    url =f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={n}&appid={weather_key}"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        #print(json.dumps(data,indent=4))
        extracted_data = []
        for location in data:
            extracted_info = {
            "name": location["name"],
            "lat": location["lat"],
                "lon": location["lon"],
            "country": location["country"],
            "state": location["state"]
            }
            extracted_data.append(extracted_info)

        return(extracted_data)
    else:
        print(f"Failed to retrieve data: HTTP {response.status_code}")

geocoding_tool = FunctionTool.from_defaults(fn=geocoding)

def current_weather(lat: float, lon: float,units:str) -> str:
    """returns the location's coordinates, current weather conditions (rain), temperature details, atmospheric pressure, humidity, wind speed and direction, cloudiness, rain volume, visibility, and times for sunrise and sunset."""
    url =f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_key}&units={units}"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # print(json.dumps(data,indent=4))
        extracted_data=extract_weather_info(data,units)
        return(extracted_data)
    else:
        return(f"Failed to retrieve data: HTTP {response.status_code}")

current_weather_tool = FunctionTool.from_defaults(fn=current_weather)



df = pd.read_csv(csv_file,low_memory=False)
pandas_engine = PandasQueryEngine(df=df, verbose=True)
Geography_tool = QueryEngineTool(
query_engine=pandas_engine,
metadata=ToolMetadata(
name="Geography",
description=".Query engine for talking to database containing name of city(Name),State Code for USA(state),(country_code),(longitude),(latitude),Country name(Country)",
)
)



def closest_cities(lat: float, lon: float, n: int) -> str:
    """Returns the n nearest cities, their latitude, and longitude to the coordinates passed to the function."""
    # Convert latitudes and longitudes to radians for vectorized Haversine calculation
    lat_radians = np.radians(df['latitude'].values)
    lon_radians = np.radians(df['longitude'].values)
    
    # Convert the input coordinates to radians
    lat_input = np.radians(lat)
    lon_input = np.radians(lon)
    
    # Vectorized Haversine formula
    dlat = lat_radians - lat_input
    dlon = lon_radians - lon_input
    a = np.sin(dlat / 2) ** 2 + np.cos(lat_input) * np.cos(lat_radians) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    # Radius of Earth in kilometers (6371 km)
    distances = 6371 * c
    
    # Add distances to the DataFrame
    df['distance'] = distances
    
    # Sort by distance and get the n closest cities
    closest_cities = df.sort_values(by='distance').head(n)
    
    # Format and return the result
    result = closest_cities[['name', 'latitude', 'longitude', 'distance']].to_string(index=False)
    
    return result

closest_cities_tool = FunctionTool.from_defaults(fn=closest_cities)


def day5_hour3_forecast(lat: float, lon: float,units:str="metric") -> str:
    """weather forecast for the next 5 days with data for every 3 hours by geographic coordinates. returns the location's coordinates, current weather conditions (rain), temperature details, atmospheric pressure, humidity, wind speed and direction, cloudiness, rain volume, visibility, and times for sunrise and sunset."""
    url =f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={weather_key}&units={units}"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # print(json.dumps(data,indent=4))
        extracted_data=process_weather_data(data,units)
        return(extracted_data)
    else:
        return(f"Failed to retrieve data: HTTP {response.status_code}")

day5_hour3_forecast_tool = FunctionTool.from_defaults(fn=day5_hour3_forecast)

current_datetime_tool = FunctionTool.from_defaults(fn=get_current_datetime)