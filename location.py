from urllib.request import urlopen
import json

class Location:
    def __init__(self):
        self.lat = ""
        self.lon = ""
        self.get_loc()

    def get_geo(self):
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        return json.load(response)

    def get_loc(self):
        geo = self.get_geo()
        self.lat = geo["loc"].split(",")[0]
        self.lon = geo["loc"].split(",")[1]

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon