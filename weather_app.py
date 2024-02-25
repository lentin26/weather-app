from flask import Flask, jsonify
# import pymysql
# import redis
import time
import json
from FetchGeo import FetchGeo
from db_config import get_redis_connection, get_mysql_connection
from flask_restx import Api, Resource, fields
import requests

from dotenv import load_dotenv
import os

# get environmental vars
load_dotenv()
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")  # key for weather api

# https://app.tomorrow.io/home
app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Maria's Flask App using Redis",
    description="A simple API to demonstrate the power of RestAPI using Redis and MySQL",
)

# weather API url 
URL = 'https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466&apikey=Spkfris4dB0T2vgoA63St81ITDEfLubv'

weather_api = api.model(
    "Film",
    {
        "us_city": fields.Integer(description="United States City", required=True, example=2),
    },
)

# Establish database connections
redis_conn = get_redis_connection()

@api.route("/weatherforecast/<str:us_city>", methods=["GET"])
class WeatherForecast(Resource):
    @api.doc(model=[weather_api])
    def get(us_city):
        """Read data from weather API, transform, write to Redis

        Args:
            film_id (int): The ID of the film.

        Returns:
            json: Actor details and other films they have acted in, along with the source and time taken.
        """
        # check cache
        city_key = f"film:{us_city}"
        lat, long = redis_conn.hgetall(city_key)

        # if not in cache go to API
        if not city_key:
            # get lat and long coordinates
            lat, long = FetchGeo(city_key)

            # format url with city latitude and longitude
            URL = 'https://api.tomorrow.io/v4/weather/forecast?location={lat},{long}&apikey={WEATHER_API_KEY}'\
                .format(lat=lat, long=long, WEATHER_API_KEY=WEATHER_API_KEY)

            r = requests.get(URL)
            city_data = r.json()

            # write data to redis
            redis_conn.hmset(city_key, city_data)
            redis_conn.expire(city_key, 3600)  # Cache for 3600 secs
            city = city_data
            source = "WeatherAPI"

        return r.json()