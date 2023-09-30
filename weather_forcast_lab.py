import requests

import os

from pprint import pprint

from datetime import datetime

import logging

# Environment API key stored in my local machine
key = os.environ.get('WEATHER_KEY')

# Open Weather map API forecast URL
url = 'https://api.openweathermap.org/data/2.5/forecast'


def main():

   # Configure logger
    logging.basicConfig(filename='debug.log', level=logging.DEBUG,
                        format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Get users input to request for URL api
    users_location = location()

    # Request and fetch the weather information with the users given API key and their location request
    weather_forecast_data, error = Request_weather_forecast(
        users_location, key)

    if error:
        # if error requesting to server, print message to users
        print('Error getting weather')

    else:
        try:
            get_forecast(weather_forecast_data)

        except Exception as e:
            # Developer error log
            logging.error(e)

            print('Error fetching forecast data ')


# Getting users location and using  while loop if users didn't input correct location params

def location():
    # Fill in the variables keys when users type in their response
    city, country = '', ''

    # Error handling where users need to type in something
    while len(city) == 0:
        city = input('Enter the city: ').strip()

    while len(country) != 2 or not country.isalpha():
        country = input('Enter the country: ').strip()

    # String to put in the url and return back
    location = f'{city},{country}'

    return location


# Requests to server to get data for openWeather api

def Request_weather_forecast(users_location, key):
    try:
        query = {'q': users_location, 'units': 'imperial', 'appid': key}

        response = requests.get(url, params=query)

        # Handle exceptions for users bad requests or server error
        response.raise_for_status()

        data = response.json()

        return data, None

    # This would catch errors failing for  the response
    except Exception as ex:

        logging.error(ex)

        print('Error REQUEST')

        return None, ex


# Get the 5 day forecast of users requested location and display it on each line from the response back on the API call

def get_forecast(weather_forecast_data):
    try:
        forecast_list = weather_forecast_data['list']

        # pprint(forecast_list) All of that locations forecast's data

        for forecast in forecast_list:

            # Temperature in main structure
            temperature = forecast['main']['temp']

            # Description in the first index of weather section
            weather_description = forecast['weather'][0]['description']

            # Wind speed
            wind_speed = forecast['wind']['speed']

            # Time in UTC
            time = forecast['dt']

            forecast_time = datetime.fromtimestamp(time)

            # Using UTC for across any time zones rather having to convert for example Minnesota's local time for someone else from a different timezone. So users wouldn't  get confused that 5pm at Minnesota is not 5pm in another timezone.
            print(f'At {forecast_time} UTC, temp will be {temperature} F with {weather_description} and wind speed of {wind_speed} miles per hour!')
            print()

    except KeyError:
        logging.error('KeyError: Format Error')
        print('Error getting weather data')


if __name__ == '__main__':
    main()
