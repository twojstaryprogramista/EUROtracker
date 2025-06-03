from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from utils.names import WindowValues
from view.controls_panel import ControlsPanel
from view.map import MapView
from utils.geo_renderer import GeoRenderer
from view.slider import Slider
# Utworzenie aplikacji
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt



class Window(QWidget):
    def __init__(self):
        super().__init__()
        g = GeoRenderer()
        self.set_ui()

        # Pokazanie okna
    def set_ui(self):
        self.setWindowTitle(WindowValues.APP_NAME.value)
        self.setWindowFlags(Qt.Window |
                    Qt.WindowTitleHint |
                    Qt.WindowMinimizeButtonHint |
                    Qt.WindowCloseButtonHint)  # tylko przycisk zamykania i tytuł

        self.setFixedSize(800, 500)  # (x, y, szerokość, wysokość)

        self.controls_panel = ControlsPanel()
        self.workspace = MapView()
        self.slider = Slider()


        self.layout = QVBoxLayout()
        
        self.layout.setSpacing(0)        # odstęp między widgetami = 0
        self.layout.setContentsMargins(0, 0, 0, 0)  # marginesy wewnątrz layoutu = 0
        self.layout.addWidget(self.controls_panel)
        self.layout.addWidget(self.workspace)
        self.layout.addWidget(self.slider)
        self.layout.addSpacing(20)



        self.setLayout(self.layout)
#window = Window()

