import os
import pandas as pd
from abc import ABC, abstractmethod
from utils.names import ModelValues


class BaseTransformer:
    def transform(self, df):
        raise NotImplementedError

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


# Zakładam, że ExcelReader jest zaimplementowany gdzieś indziej i działa poprawnie
# z metodą read zwracającą pd.DataFrame
class ExcelReader:
    def __init__(self, base_dir="resources/data"):
        self.base_dir = base_dir

    def read(self, file_name: str, sheet_name: str, skiprows=0) -> pd.DataFrame:
        file_path = os.path.join(self.base_dir, file_name)
        try:
            return pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows)
        except FileNotFoundError as e:
            raise RuntimeError(f"Nie znaleziono pliku: {file_path}") from e

# Mock funkcji readElectricVehicles i readEndOfLifeVechicles, zakładając użycie ExcelReader
def read_electric_vehicles() -> list:
    reader = ExcelReader()
    df = reader.read("tran_r_elvehst.xlsx", "Sheet 3", skiprows=0) # Dostosuj nazwy plików/arkuszy
    transformer = ElectricVehiclesTransformer()
    return transformer.transform(df)

def read_end_of_life_vehicles() -> list:
    reader = ExcelReader()
    df = reader.read("env_waselvt.xlsx", "Sheet 1", skiprows=0) # Dostosuj nazwy plików/arkuszy
    transformer = EndOfLifeVehicleTransformer()
    return transformer.transform(df)



        # map_object.save(self._save_path) # Odkomentuj, jeśli to rzeczywisty obiekt mapy
# koniec mocków


# utils/data_loader.py (nowy moduł dla ładowania danych)
import json
import os
import pandas as pd
from typing import Dict, Any, List

# Zakładam, że ExcelReader i transformery są zdefiniowane i importowane poprawnie
# from your_excel_reader_module import ExcelReader
# from your_transformers_module import EndOfLifeVehicleTransformer, ElectricVehiclesTransformer
# from utils.names import ModelValues # Importuj z odpowiedniego miejsca

class DataLoader:
    """
    Klasa odpowiedzialna za ładowanie i wstępne przetwarzanie danych z różnych źródeł.
    Zgodna z SRP, skupia się tylko na ładowaniu.
    """
    def __init__(self, excel_reader: ExcelReader):
        self._excel_reader = excel_reader
        self._eol_transformer = EndOfLifeVehicleTransformer()
        self._electric_transformer = ElectricVehiclesTransformer()

    def load_end_of_life_vehicles_data(self):
        """Ładuje i transformuje dane o pojazdach wycofanych z eksploatacji."""
        df = self._excel_reader.read("env_waselvt.xlsx", "Sheet 1") # Nazwa pliku i arkusza
        return self._eol_transformer.transform(df)

    def load_electric_vehicles_data(self):
        """Ładuje i transformuje dane o pojazdach elektrycznych."""
        df = self._excel_reader.read("tran_r_elvehst.xlsx", "Sheet 3") # Nazwa pliku i arkusza
        return self._electric_transformer.transform(df)

    def load_geojson_data(self, file_path: str, filter_level: int = None):
        """Ładuje dane GeoJSON i opcjonalnie filtruje je."""
        full_path = str(file_path) # Upewnij się, że ModelValues.XXX.value jest stringiem
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Plik GeoJSON nie istnieje: {full_path}")
        
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if filter_level is not None:
            features = [f for f in data.get("features", []) if f.get("properties", {}).get("LEVL_CODE") == filter_level]
            return {"type": "FeatureCollection", "features": features}
        return data
