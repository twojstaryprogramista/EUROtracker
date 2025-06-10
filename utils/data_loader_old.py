import os
import pandas as pd
from abc import ABC, abstractmethod
from utils.names import ModelValues

class ExcelReader:
    def __init__(self, base_dir="resources/data"):
        self.base_dir = base_dir

    def read(self, file_name: str, sheet_name: str, skiprows=0) -> pd.DataFrame:
        file_path = os.path.join(self.base_dir, file_name)
        try:
            return pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows)
        except FileNotFoundError as e:
            raise RuntimeError(f"Nie znaleziono pliku: {file_path}") from e

class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, df: pd.DataFrame) -> list:
        pass
    

class EndOfLifeVehicleTransformer(BaseTransformer):
    def transform(self, df):
        data_list = []
        for _, row in df.iterrows():
            country_name = row.iloc[0]
            values = []
            for year, col in zip(range(ModelValues.END_OF_LIFE_VEHICLES_RANGE_MIN.value, ModelValues.END_OF_LIFE_VEHICLES_RANGE_MAX.value+1), range(1, 21, 2)):
                values.append({'year': year, 'value': row.iloc[col]})
            data_list.append({'country': country_name, 'values': values})
        
        return data_list
    
class ElectricVehicleTransformer(BaseTransformer):
    def transform(self, df):
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
        



class VehicleDataLoader:
    def __init__(self, reader: ExcelReader, transformer: BaseTransformer):
        self.reader = reader
        self.transformer = transformer

    def load(self, file_name: str, sheet_name: str, skiprows=0) -> list:
        df = self.reader.read(file_name, sheet_name, skiprows)
        return self.transformer.transform(df)
    



def readEndOfLifeVechicles():

    loader1 = VehicleDataLoader(ExcelReader(), EndOfLifeVehicleTransformer())
    return loader1.load("env_waselvt.xlsx", "Sheet 1", skiprows=10)
def readElectricVehicles():
    # Electric vehicles
    loader2 = VehicleDataLoader(ExcelReader(), ElectricVehicleTransformer())
    return loader2.load("tran_r_elvehst.xlsx", "Sheet 3", skiprows=10)