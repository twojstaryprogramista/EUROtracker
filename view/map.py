from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from utils.names import ModelValues


class MapView(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.load(QUrl.fromLocalFile(str(ModelValues.MAP_DIR.value)))

    def reload(self):
        self.load(QUrl.fromLocalFile(str(ModelValues.MAP_DIR.value)))
class MapViewRegions(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.load(QUrl.fromLocalFile(str(ModelValues.REGIONS_MAP_DIR.value)))

    def reload(self):
        self.load(QUrl.fromLocalFile(str(ModelValues.REGIONS_MAP_DIR.value)))