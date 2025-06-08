import pandas as pd
import os

def read_excel_data(file_name, sheet_name, skiprows=0) -> pd.DataFrame:
    file_path = os.path.join("resources", "data", file_name)
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows)
    return df

def readEndOfLifeVechicles() -> list:
    raw_data = read_excel_data('env_waselvt.xlsx', 'Sheet 1', skiprows=10)
    cleaned_data = raw_data

    data_list = []

    for _, row in cleaned_data.iterrows():

        country_name = row.iloc[0]
        values = []
        col_index = 1
        for year in range(2013, 2023):
            value = row.iloc[col_index]

            values.append({
                'year': year,
                'value': value
            })
            col_index += 2
        data_list.append({
            'country': country_name,
            'values': values
        })
    print(data_list)
    return data_list[:30]

def readElectricVehicles() -> list:
    raw_data = read_excel_data('tran_r_elvehst.xlsx', 'Sheet 1', skiprows=10)
    cleaned_data = raw_data

    data_list = []

    for _, row in cleaned_data.iterrows():
        geo_code = row.iloc[0]
        geo_label = row.iloc[1]

        values = []

        col_index = 2
        for year in range(2018, 2023):
            value = row.iloc[col_index]

            values.append({
                'year': year,
                'value': value
            })
            col_index += 2

        data_list.append({
            'geo_code': geo_code,
            'geo_label': geo_label,
            'values': values
        })

    return data_list[:386]

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


def get_value_for_year(self, country, year):
    for entry in country['values']:
        
        if entry['year'] == year:
            value = entry['value']
            if isinstance(value, (int, float)):
                return value
            else:
                print(f"Invalid value for {country['country']} in {year}: {value}")
                return 0  # lub None jeśli chcesz
    print(f"No data for {country['country']} in {year}")
    return 0  # jeśli nie ma danego roku






def set_values(self, value):
    #GeoRenderer.slider_from = value[0]
    #GeoRenderer.slider_to = value[1]

    #self.values[self.countries.index('Poland')]= value[0]

    #go trough all countries and set value from eol using country name as key
    for country in self.eol_data:
        if country['country'] in self.countries:
            #print(f"Setting value for {country['country']}")
            #self.values[self.countries.index(country['country'])] = GeoRenderer.get_sum_for_country_in_range(country, GeoRenderer.slider_from, GeoRenderer.slider_to)
            
            self.values[self.countries.index(country['country'])] = self.get_value_for_year(country,value)

    self.map_creator_countries.set_values(self.values)
    self.file_manager.save_html(self.map_creator_countries.get_map())


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