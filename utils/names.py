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

class SliderValues(Enum):
    MIN = 2001
    MAX = 2025



class ModelValues(Enum):
    SCRIPT_DIR = Path(__file__).resolve().parent.parent
    MAP_DIR = SCRIPT_DIR / "resources" / "map.html"
    GEO_DATA_DIR = SCRIPT_DIR / "resources" / "europa.geojson"


    

