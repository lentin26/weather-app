
import pandas as pd

class FetchGeo:
    def __init__(self, data_loc):

        self.data = pd.read(data_loc)

    def get_lat_long(self, us_city):
        """

        """
        # get lat and long coordinates
        lat, long = self.data.loc[
            self.data.city.str.lower() == us_city.lower(), 
            ['longitude', 'latitude']
        ].to_numpy().flatten().tolist()