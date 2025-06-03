

# do testu
#
#
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget,QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pathlib import Path



# do testu
#
#

class MapView(QWebEngineView):
    def __init__(self):
        script_dir = str(Path(__file__).resolve().parent.parent)
        super().__init__()
        print(script_dir+'\\mapa.html')
        self.load(QUrl.fromLocalFile(script_dir+'\\utils\\mapa.html'))  # Ścieżka do pliku HTML