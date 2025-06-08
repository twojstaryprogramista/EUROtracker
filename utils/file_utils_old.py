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