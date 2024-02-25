
if __name__ == "__main__":
    import pandas as pd
    import matplotlib.pyplot as plt
    import requests
    
    # get forecast for Northampton
    us_city = "northampton"
    r = requests.get('http://127.0.0.1:8000//weatherforecast/{us_city}'.format(us_city=us_city))

    # normalize data
    data = pd.json_normalize(r.json()['data']['timelines']['minutely'])
    data['time'] = pd.to_datetime(data['time'])

    # return wind speed forecast plot
    plt.plot(data.time, data['values.windSpeed'])

    # add labels
    plt.title(us_city)
    plt.xlabel('data')
    plt.ylabel('wind speed')

    plt.show()