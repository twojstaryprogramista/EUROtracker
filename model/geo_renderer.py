from utils.names import SliderValues
from model.map_creator import MapCreatorCountries, MapCreatorRegions
from utils.file_manager import FileManager

class GeoRenderer:
    
    def update_for_year(self,year):
        values = self.file_manager.get_values_for_year_countries(year)
        self.map_creator_countries.set_values(values)
        self.file_manager.save_countries_map(self.map_creator_countries.get_map())
    def update_for_year_regions(self,year):
        values = self.file_manager.get_values_for_year_regions(year)
        self.map_creator_regions.set_values(values)
        self.file_manager.save_regions_map(self.map_creator_regions.get_map())
    def __init__(self):
        self.file_manager = FileManager()

        #self.save_path = str(ModelValues.MAP_DIR.value)
        self.geojson_data=self.file_manager.get_geojson_data_countries()
        
        #implementacja MapCreator
        self.map_creator_countries = MapCreatorCountries(self.geojson_data)


        self.geojson_data_regions = self.file_manager.get_geojson_data_regions()
        self.map_creator_regions = MapCreatorRegions(self.geojson_data_regions)
        
        regions_values = self.file_manager.get_values_for_year_regions(2020)
        self.map_creator_regions.set_values(regions_values)
        self.file_manager.save_regions_map(self.map_creator_regions.get_map())

        self.countries = [feature["properties"]["NAME"] for feature in self.geojson_data["features"]]
        self.values = [0] * len(self.countries)
        #self.values[self.countries.index('Poland')]=200
        #self.set_values([SliderValues.SLIDER_DEFAULT_MIN.value,SliderValues.SLIDER_DEFAULT_MAX.value])
        countries_values = self.file_manager.get_values_for_year_countries(SliderValues.SLIDER_DEFAULT_MIN.value)
        self.map_creator_countries.set_values(countries_values)
        self.file_manager.save_countries_map(self.map_creator_countries.get_map())
        



    
    



