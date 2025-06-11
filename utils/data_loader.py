import os
import pandas as pd
from abc import ABC, abstractmethod
from utils.names import ModelValues

#WZORZEC STRATEGIA
class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, df: pd.DataFrame):
        pass

class ElectricVehiclesTransformer(BaseTransformer):
    def transform(self, df: pd.DataFrame):
        data_list = []
        for _, row in df.iterrows():
            geo_code = row.iloc[0]
            geo_label = row.iloc[1]
            values = []
            for year, col in zip(range(ModelValues.ELECTRIC_VEHICLES_RANGE_MIN.value, ModelValues.ELECTRIC_VEHICLES_RANGE_MAX.value+1), range(2, 12, 2)):
                values.append({'year': year, 'value': row.iloc[col]})
            data_list.append({
                'geo_code': geo_code,
                'geo_label': geo_label,
                'values': values
            })
        return data_list

class EndOfLifeVehicleTransformer(BaseTransformer):
    def transform(self, df: pd.DataFrame):
        data_list = []
        for _, row in df.iterrows():
            country_name = row.iloc[0]
            values = []
            for year, col in zip(range(ModelValues.END_OF_LIFE_VEHICLES_RANGE_MIN.value, ModelValues.END_OF_LIFE_VEHICLES_RANGE_MAX.value+1), range(1, 21, 2)):
                values.append({'year': year, 'value': row.iloc[col]})
            data_list.append({'country': country_name, 'values': values})
        
        return data_list

class ExcelReader:
    def __init__(self, base_dir="resources/data"):
        self.base_dir = base_dir

    def read(self, file_name: str, sheet_name: str, skiprows=0) -> pd.DataFrame:
        file_path = os.path.join(self.base_dir, file_name)
        try:
            return pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows)
        except FileNotFoundError as e:
            raise RuntimeError(f"Nie znaleziono pliku: {file_path}") from e

def read_electric_vehicles() -> list:
    reader = ExcelReader()
    df = reader.read("tran_r_elvehst.xlsx", "Sheet 3", skiprows=0)
    transformer = ElectricVehiclesTransformer()
    return transformer.transform(df)

def read_end_of_life_vehicles() -> list:
    reader = ExcelReader()
    df = reader.read("env_waselvt.xlsx", "Sheet 1", skiprows=0)
    transformer = EndOfLifeVehicleTransformer()
    return transformer.transform(df)


import json
import os
import pandas as pd
from typing import Dict, Any, List

class DataLoader:
    def __init__(self, excel_reader: ExcelReader):
        self._excel_reader = excel_reader
        self._eol_transformer = EndOfLifeVehicleTransformer()
        self._electric_transformer = ElectricVehiclesTransformer()

    def load_end_of_life_vehicles_data(self):
        df = self._excel_reader.read("env_waselvt.xlsx", "Sheet 1")
        return self._eol_transformer.transform(df)

    def load_electric_vehicles_data(self):
        df = self._excel_reader.read("tran_r_elvehst.xlsx", "Sheet 3")
        return self._electric_transformer.transform(df)

    def load_geojson_data(self, file_path: str, filter_level: int = None):
        full_path = str(file_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Plik GeoJSON nie istnieje: {full_path}")
        
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if filter_level is not None:
            features = [f for f in data.get("features", []) if f.get("properties", {}).get("LEVL_CODE") == filter_level]
            return {"type": "FeatureCollection", "features": features}
        return data
