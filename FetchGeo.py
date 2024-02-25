
import pandas as pd

class FetchGeo:
    def __init__(self, data_loc):

        self.data = pd.read_csv(data_loc)

    def get_lat_long(self, us_city):
        """Read data from weather API, transform, write to Redis

        Args:
            us_city (str): The name of the city.

        Returns:
            json: Actor details and other films they have acted in, along with the source and time taken.
        """
        # get lat and long coordinates
        lat, long = self.data.loc[
            self.data.city.str.lower() == us_city.lower(), 
            ['longitude', 'latitude']
        ].to_numpy().flatten().tolist()

        return lat, long