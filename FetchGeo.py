
import pandas as pd

class FetchGeo:
    def __init__(self, data_loc):

        self.data = pd.read_csv(data_loc)

    def get_lat_long(self, us_city):
        """Read data locally, lookup latitude, longitude of united states city

        Args:
            us_city (str): The name of the city.

        Returns:
            lat (float): latitude of united states city
            long (float): longitude of united states city
        """
        # get lat and long coordinates
        lat, long = self.data.loc[
            self.data.city.str.lower() == us_city.lower(), 
            ['longitude', 'latitude']
        ].to_numpy().flatten().tolist()

        return lat, long