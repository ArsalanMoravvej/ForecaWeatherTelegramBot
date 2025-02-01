import requests
from bs4 import BeautifulSoup
import json
import re
from typing import List
from .models import Location, HourlyWeather, DailyWeather


class ForecaError(Exception):
    """Base exception for Foreca weather service"""
    pass

class APIRequestError(ForecaError):
    """Raised when API request fails"""
    pass

class NoResultsError(ForecaError):
    """Raised when no results are found"""
    pass

class ParsingError(ForecaError):
    """Raised when there's an error parsing the response"""
    pass


def find_location(query: str, limit: int = 5) -> List[Location]:

    url: str = f"https://api.foreca.net/locations/search/{query}.json?limit={limit}"

    try:
        response: requests.models.Response = requests.get(url=url)
        response.raise_for_status()  # This will raise an exception for undesirable status codes
    except requests.exceptions.RequestException as e:
        raise APIRequestError(f"Failed to fetch location data: {str(e)}")

    data = response.json()
    if not data.get("results"):
        raise NoResultsError(f"No locations found for query: {query}")
    
    return [Location(**loc) for loc in data["results"]]



def fetch_daily_weather(location: Location) -> List[DailyWeather]:
    url_string = f"https://api.foreca.net/data/favorites/{location.id}.json"

    try:
        response: requests.models.Response = requests.get(url=url_string)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise APIRequestError(f"Failed to fetch daily weather data: {str(e)}")

    data = response.json()
    if not data:
        raise NoResultsError(f"No daily weather data found for location: {location.name}")
    
    if not data.get(location.id):
        raise NoResultsError(f"No data found for location ID: {location.id}")
    
    return [DailyWeather(location_info=location, **daily_data) 
            for daily_data in data[location.id]]


    

def fetch_hourly_weather(location: Location, day: int = 0) -> List[HourlyWeather]:

    url_string = f"https://www.foreca.com/{location.id}/" + \
        f"{location.name}-{location.countryName}/hourly?day={day}"
    
    try:
        response: requests.models.Response = requests.get(url=url_string)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise APIRequestError(f"Failed to fetch hourly weather data: {str(e)}")

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', string=re.compile('renderHourly'))
        
        if not script_tag:
            raise ParsingError("Could not find weather data in the page")

        match = re.search(r'data:\s*(\[\{.*?\}\])', script_tag.string)
        if not match:
            raise ParsingError("Could not extract weather data from the script")
        
        weather_data = json.loads(match.group(1))
        
        if not weather_data:
            raise NoResultsError(f"No hourly weather data found for location: {location.name}")
        
    except (json.JSONDecodeError, AttributeError) as e:
        raise ParsingError(f"Error parsing hourly weather data: {str(e)}")
    
    return [HourlyWeather(location_info=location, **hourly_data) 
            for hourly_data in weather_data]