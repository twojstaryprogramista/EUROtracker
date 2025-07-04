from utils.data_loader import ExcelReader
from utils.names import ModelValues
from model.html_creator import HTMLCreator
from utils.data_loader import DataLoader
from model.html_creator import HTMLCreator
from utils.names import ModelValues 


class ValuesOrganizer:
    def __init__(
        self,
        eol_data,
        country_names,
        electric_vehicle_data,
        region_names
    ):
        self._eol_data = eol_data
        self._country_names = country_names
        self._electric_vehicle_data = electric_vehicle_data
        self._region_names = region_names

    def get_values_for_year_regions(self, year):
        values_for_regions = []
        for region_name in self._region_names:
            
            region_data = next((item for item in self._electric_vehicle_data if item['geo_label'] == region_name), None)
            if region_data is None:
                values_for_regions.append(0)
                continue
            
            year_entry = next((entry for entry in region_data['values'] if entry['year'] == year), None)
            if year_entry is None:
                values_for_regions.append(0)
                continue
            
            val = year_entry['value']
            if isinstance(val, (int, float)):
                values_for_regions.append(val)
            else:
                values_for_regions.append(0)
        
        return values_for_regions

    def get_values_for_year_countries(self, year):
        values = [0] * len(self._country_names)
        for country in self._eol_data:
            name = country.get('country')
            if name in self._country_names:
                value = next(
                    (
                        v["value"] for v in country.get("values", [])
                        if v.get("year") == year and isinstance(v.get("value"), (int, float))
                    ),
                    0
                )

                if value == 0:
                    print(f"Missing or invalid value for {name} in {year}")

                values[self._country_names.index(name)] = value
        return values


class MapManager:
    def __init__(self, countries_html_creator, regions_html_creator):
        self._countries_html_creator = countries_html_creator
        self._regions_html_creator = regions_html_creator

    def save_countries_map(self, map_object):
        self._countries_html_creator.save(map_object)

    def save_regions_map(self, map_object):
        self._regions_html_creator.save(map_object)



#WZORZEC FASADY
#WZORZEC SINGLETON
class FileManager:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            excel_reader = ExcelReader()
            data_loader = DataLoader(excel_reader)

            self._eol_data = data_loader.load_end_of_life_vehicles_data()
            self._electric_vehicle_data = data_loader.load_electric_vehicles_data()
            
            self._geojson_data_countries = data_loader.load_geojson_data(ModelValues.COUNTRIES_DATA_DIR.value)
            self._country_names = [f["properties"]["NAME"] for f in self._geojson_data_countries["features"]]

            self._geojson_data_regions = data_loader.load_geojson_data(ModelValues.REGIONS_DATA_DIR.value, filter_level=2)
            self._region_names = [f["properties"]["NUTS_NAME"] for f in self._geojson_data_regions["features"]]

            self._value_organizer = ValuesOrganizer(
                self._eol_data,
                self._country_names,
                self._electric_vehicle_data,
                self._region_names
            )

            countries_html_creator = HTMLCreator() 
            countries_html_creator.set_save_path(ModelValues.MAP_DIR.value)
            regions_html_creator = HTMLCreator()
            regions_html_creator.set_save_path(ModelValues.REGIONS_MAP_DIR.value)

            self._map_manager = MapManager(countries_html_creator, regions_html_creator)

            self._years_countries = list(range(ModelValues.END_OF_LIFE_VEHICLES_RANGE_MIN.value, ModelValues.END_OF_LIFE_VEHICLES_RANGE_MAX.value + 1))
            self._years_regions = list(range(ModelValues.ELECTRIC_VEHICLES_RANGE_MIN.value, ModelValues.ELECTRIC_VEHICLES_RANGE_MAX.value + 1))

    def get_country_names(self):
        return self._country_names

    def get_region_names(self):
        return self._region_names

    def get_eol_data(self):
        return self._eol_data

    def get_electric_vehicle_data(self):
        return self._electric_vehicle_data

    def get_geojson_data_countries(self):
        return self._geojson_data_countries

    def get_geojson_data_regions(self):
        return self._geojson_data_regions
    
    def get_years_countries(self):
        return self._years_countries

    def get_years_regions(self):
        return self._years_regions

    def get_values_for_year_regions(self, year: int):
        return self._value_organizer.get_values_for_year_regions(year)

    def get_values_for_year_countries(self, year: int):
        return self._value_organizer.get_values_for_year_countries(year)

    def save_countries_map(self, map_object):
        self._map_manager.save_countries_map(map_object)

    def save_regions_map(self, map_object):
        self._map_manager.save_regions_map(map_object)