import pandas as pd
import matplotlib.pyplot as plt
import requests


class VisualizeWeather:

    def __init__(self):
        pass

    def visualize_windspeed_forecast(self, us_city="northampton"):
        """Read data from weather API, transform, write to Redis

        Args:
            us_city (str): The name of the city.

        Returns:
            plot of forecasted wind speed in days
        """

        # us_city = "northampton"
        r = requests.get('http://127.0.0.1:8000//weatherforecast/{us_city}'.format(us_city=us_city))

        # normalize weather forecast data
        data = pd.json_normalize(r.json()['data']['timelines']['minutely'])
        data['time'] = pd.to_datetime(data['time'])

        # return wind speed forecast plot
        plt.plot(data.time, data['values.windSpeed'])

        # add labels
        plt.title(us_city)
        plt.xlabel('data')
        plt.ylabel('wind speed')
        
        plt.show()