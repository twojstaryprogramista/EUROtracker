import plotly.express as px
import json
#from utils.file_utils_old import readElectricVehicles, readEndOfLifeVechicles

from utils.names import MapValues, ModelValues, SliderValues
from model.html_creator import HTMLCreator
from view.map import MapView
from model.map_creator import MapCreatorCountries, MapCreatorRegions
from utils.file_manager import FileManager, ValuesOrganizer

class GeoRenderer:

    #eol_data = []
    #electrical_data = []

    slider_from = 2013
    slider_to = 2022




        #self.fig = self.__map_setup()
        #self.html_creator.save(self.fig)


    def set_values_for_year(self, year: int):
        for country in self.eol_data:
            name = country.get('country')
            if name in self.countries:
                value = next(
                    (
                        v["value"] for v in country.get("values", [])
                        if v.get("year") == year and isinstance(v.get("value"), (int, float))
                    ),
                    0
                )

                if value == 0:
                    print(f"Missing or invalid value for {name} in {year}")

                self.values[self.countries.index(name)] = value
        self.map_creator_countries.set_values(self.values)
        self.file_manager.save_html(self.map_creator_countries.get_map())

    def update_for_year(self,year):
        values = self.file_manager.value_organizer.get_values_for_year_countries(year)
        self.map_creator_countries.set_values(values)
        self.file_manager.save_html(self.map_creator_countries.get_map())

    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.eol_data = self.file_manager.get_eol_data()
        self.electrical_data = self.file_manager.get_electrical_data()

        #self.save_path = str(ModelValues.MAP_DIR.value)
        self.geojson_data=self.file_manager.get_geojson_data_countries()
        
        #implementacja MapCreator
        self.map_creator_countries = MapCreatorCountries(self.geojson_data)


        self.geojson_data_regions = self.file_manager.get_geojson_data_regions()
        self.map_creator_regions = MapCreatorRegions(self.geojson_data_regions)
        
        self.map_creator_regions.set_values(self.file_manager.value_organizer.get_values_for_year(self.electrical_data,[f["properties"]["NUTS_NAME"] for f in self.geojson_data_regions["features"]],2020))


        self.countries = [feature["properties"]["NAME"] for feature in self.geojson_data["features"]]
        self.values = [0] * len(self.countries)
        #self.values[self.countries.index('Poland')]=200
        #self.set_values([SliderValues.SLIDER_DEFAULT_MIN.value,SliderValues.SLIDER_DEFAULT_MAX.value])
        self.set_values_for_year(SliderValues.SLIDER_DEFAULT_MIN.value)
        self.file_manager.save_html(self.map_creator_countries.get_map())
        
        self.file_manager.save_html_regions(self.map_creator_regions.get_map())


    
    



