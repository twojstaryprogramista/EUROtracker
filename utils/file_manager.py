from utils.file_utils import readElectricVehicles, readEndOfLifeVechicles
from utils.names import MapValues, ModelValues, SliderValues
from model.html_creator import HTMLCreator
import json

class FileManager:
    def __init__(self):
        self.eol_data = readEndOfLifeVechicles()

        self.geojson_data_regions = self.__load_and_filter_geojson()
        self.indexes_regions = [f["properties"]["NUTS_NAME"] for f in self.geojson_data_regions["features"]]


        self.electrical_data = readElectricVehicles()
        self.html_creator = HTMLCreator()
        self.html_creator_regions = HTMLCreator()
        self.html_creator_regions.set_save_path(ModelValues.REGIONS_MAP_DIR.value)
        with open(
        str(ModelValues.COUNTRIES_DATA_DIR.value), "r", encoding="utf-8") as f:
            self.geojson_data_countries = json.load(f)
        self.indexes_countries = [feature["properties"]["NAME"] for feature in self.geojson_data_countries["features"]]
        self.value_organizer = ValuesOrganizer(self.eol_data,self.indexes_countries,self.electrical_data,self.indexes_regions)

        #print(self.indexes)
    def get_eol_data(self):
        return self.eol_data
    
    def get_electrical_data(self):
        return self.electrical_data
    
    def get_geojson_data_countries(self):
        return self.geojson_data_countries
    
    def __load_and_filter_geojson(self):
        with open(str(ModelValues.REGIONS_DATA_DIR.value), "r", encoding="utf-8") as f:
            data = json.load(f)

        features = [f for f in data["features"] if f["properties"]["LEVL_CODE"] == 2]
        return {"type": "FeatureCollection", "features": features}


    def get_geojson_data_regions(self):
        return self.geojson_data_regions

    def save_html(self,map):
        self.html_creator.save(map)
    def save_html_regions(self,map):
        self.html_creator_regions.save(map)

class ValuesOrganizer:
    def __init__(self,eol_data, indexes_countries, electrical_data, indexes_regions):
        self.eol_data = eol_data
        self.indexes_countries = indexes_countries
        self.electrical_data = electrical_data
        self.indexes_regions = indexes_regions

    #rla regionow    
    def get_values_for_year(self,data_list, regions, year):
        values_for_regions = []
        for region_name in regions:
            # Szukamy słownika regionu w data_list po geo_label
            region_data = next((item for item in data_list if item['geo_label'] == region_name), None)
            if region_data is None:
                # Jeśli nie ma regionu w danych, daj 0
                values_for_regions.append(0)
                continue
            
            # Szukamy wartość dla podanego roku
            year_entry = next((entry for entry in region_data['values'] if entry['year'] == year), None)
            if year_entry is None:
                values_for_regions.append(0)
                continue
            
            # Sprawdzamy wartość, jeśli nie jest liczbą, daj 0
            val = year_entry['value']
            if isinstance(val, (int, float)):
                values_for_regions.append(val)
            else:
                values_for_regions.append(0)
        
        return values_for_regions
    
    def get_values_for_year_countries(self, year: int):
        values = [0] * len(self.indexes_countries)
        for country in self.eol_data:
            name = country.get('country')
            if name in self.indexes_countries:
                value = next(
                    (
                        v["value"] for v in country.get("values", [])
                        if v.get("year") == year and isinstance(v.get("value"), (int, float))
                    ),
                    0
                )

                if value == 0:
                    print(f"Missing or invalid value for {name} in {year}")

                values[self.indexes_countries.index(name)] = value
        return values
    