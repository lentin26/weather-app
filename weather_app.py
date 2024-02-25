from flask import Flask, jsonify
import time
import json
from FetchGeo import FetchGeo
from db_config import get_redis_connection
from flask_restx import Api, Resource, fields
import requests
from dotenv import load_dotenv
import os

fetcher = FetchGeo(data_loc="data/us_cities_clean.csv")

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
        "us_city": fields.String(description="United States City", required=True, example=2),
    },
)

# Establish database connections
redis_conn = get_redis_connection()

@api.route("/weatherforecast/<us_city>", methods=["GET"])
class WeatherForecast(Resource):
    @api.doc(model=[weather_api])
    def get(self, us_city):
        """Read data from weather API, transform, write to Redis

        Args:
            us_city (str): The name of the city.

        Returns:
            json: Actor details and other films they have acted in, along with the source and time taken.
        """
        start = time.time()
        # check cache
        city_key = f"city:{us_city}"
        city_data = redis_conn.hgetall(city_key)

        if not city_data:
            # get lat and long coordinates
            lat, long = fetcher.get_lat_long(us_city)

            # format url with city latitude and longitude
            URL = 'https://api.tomorrow.io/v4/weather/forecast?location={lat},{long}&apikey={WEATHER_API_KEY}'\
                .format(lat=lat, long=long, WEATHER_API_KEY=WEATHER_API_KEY)

            r = requests.get(URL)
            city_data = r.json()

            if city_data:
                # write data to redis
                redis_conn.hset("city:northampton", "data", json.dumps(r.json()))
                # redis_conn.hmset(city_key, json.dumps(city_data))
                redis_conn.expire(city_key, 3600)  # Cache for 3600 secs
                source = "WeatherAPI"
            else:
                return jsonify({"message": "Film not found"}), 404
        else:
            source = "Redis"

        redis_conn.incr(f"city_views:{us_city}")

        end = time.time()
        time_taken = end - start

        data = json.loads(city_data["data"])
        return jsonify({"city": us_city, "source": source, "time_taken": time_taken, "data": data})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)