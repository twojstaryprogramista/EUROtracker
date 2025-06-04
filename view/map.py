

# do testu
#
#
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget,QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pathlib import Path
from utils.names import ModelValues


# do testu
#
#

class MapView(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.load(QUrl.fromLocalFile(str(ModelValues.MAP_DIR.value)))