from enum import Enum
from pathlib import Path



class WindowValues(Enum):
    APP_NAME = 'EUROtracker'
    WIDTH = 800
    HEIGHT = 500



class Style(Enum):
    BUTTON_COLOR = "#007BFF"




class MapValues(Enum):
    PUPK_VALUE = 'Ilość samochodów użytkowych'
    PEPR_VALUE = 'Ilość samochodów elektrycznych'
    HTML_EDIT =             """<head>
            <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            overflow: hidden;
        }
        .plot-container, .main-svg, .geo {
            width: 100% !important;
            height: 100% !important;
        }
        </style>"""




class ModelValues(Enum):
    SCRIPT_DIR = Path(__file__).resolve().parent.parent
    MAP_DIR = SCRIPT_DIR / "resources" / "map_countries.html"
    REGIONS_MAP_DIR = SCRIPT_DIR / "resources" / "map_regions.html"
    COUNTRIES_DATA_DIR = SCRIPT_DIR / "resources" / "countries" / "europa.geojson"
    REGIONS_DATA_DIR = SCRIPT_DIR / "resources" / "regions" / "NUTS_RG_01M_2024_4326.geojson"
    END_OF_LIFE_VEHICLES_RANGE_MIN = 2013
    END_OF_LIFE_VEHICLES_RANGE_MAX = 2022
    END_OF_LIFE_VEHICLES_DEFAULT = 2017
    ELECTRIC_VEHICLES_RANGE_MIN = 2018
    ELECTRIC_VEHICLES_RANGE_MAX = 2022
    ELECTRIC_VEHICLES_DEFAULT = 2020
    DATA_START_ROW = 10



class SliderValues(Enum):
    MIN = ModelValues.END_OF_LIFE_VEHICLES_RANGE_MIN.value
    MAX = ModelValues.END_OF_LIFE_VEHICLES_RANGE_MAX.value
    SLIDER_DEFAULT_MIN = 2019
    SLIDER_DEFAULT_MAX = 2021


