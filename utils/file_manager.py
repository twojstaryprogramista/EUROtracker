from utils.file_utils import readElectricVehicles, readEndOfLifeVechicles
from utils.names import MapValues, ModelValues, SliderValues
import json

class FileManager:
    def __init__(self):
        self.eol_data = readEndOfLifeVechicles()
        self.electrical_data = readElectricVehicles()
        with open(
        str(ModelValues.COUNTRIES_DATA_DIR.value), "r", encoding="utf-8") as f:
            self.geo = json.load(f)

    def get_eol_data(self):
        return self.eol_data
    
    def get_electrical_data(self):
        return self.electrical_data
    
    def get_geojson_data_countries(self):
        return self.geo