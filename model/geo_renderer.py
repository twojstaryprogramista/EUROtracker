import plotly.express as px
import json
#from utils.file_utils_old import readElectricVehicles, readEndOfLifeVechicles

from utils.names import MapValues, ModelValues, SliderValues
from model.html_creator import HTMLCreator
from view.map import MapView
from model.map_creator import MapCreatorCountries
from utils.file_manager import FileManager

class GeoRenderer:

    #eol_data = []
    #electrical_data = []

    slider_from = 2013
    slider_to = 2022

    def get_sum_for_country_in_range(country, from_year, to_year):
        # Filter and sum values in the given range, ignore invalid values like ':'
        total = 0
        for entry in country['values']:
            year = entry['year']
            value = entry['value']
            if from_year <= year <= to_year:
                if isinstance(value, (int, float)):
                    total += value
                else:
                    print(f"Skipping invalid value for {country['country']} in {year}: {value}")

        return total

    def set_values(self, value):
        GeoRenderer.slider_from = value[0]
        GeoRenderer.slider_to = value[1]

        #self.values[self.countries.index('Poland')]= value[0]

        #go trough all countries and set value from eol using country name as key
        for country in self.eol_data:
            if country['country'] in self.countries:
                #print(f"Setting value for {country['country']}")
                self.values[self.countries.index(country['country'])] = GeoRenderer.get_sum_for_country_in_range(country, GeoRenderer.slider_from, GeoRenderer.slider_to)

        self.map_creator_countries.set_values(self.values)
        self.html_creator.save(self.map_creator_countries.get_map())
        #self.fig = self.__map_setup()
        #self.html_creator.save(self.fig)

    def __init__(self, file_manager):
        self.eol_data = file_manager.get_eol_data()
        self.electrical_data = file_manager.get_electrical_data()

        #self.save_path = str(ModelValues.MAP_DIR.value)


        #FILE MANAGER
        self.html_creator = HTMLCreator()

        #FILE MANAGER
        self.geojson_data=file_manager.get_geojson_data_countries()

        #implementacja MapCreator
        self.map_creator_countries = MapCreatorCountries(self.geojson_data)

        self.countries = [feature["properties"]["NAME"] for feature in self.geojson_data["features"]]
        self.values = [1] * len(self.countries)
        #self.values[self.countries.index('Poland')]=200
        self.set_values([SliderValues.SLIDER_DEFAULT_MIN.value,SliderValues.SLIDER_DEFAULT_MAX.value])


    
    



