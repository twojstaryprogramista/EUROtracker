from view.main_window import Window
from PyQt5.QtWidgets import QApplication
from model.geo_renderer import GeoRenderer
from view.controls_panel import ControlsPanel
from view.map import MapView
from view.slider import Slider
import sys

class App:


    _instance = None


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
            self.app = QApplication(sys.argv)
            self.g = GeoRenderer()
            
            print("Uruchomiono")
            self.controls_panel = ControlsPanel()
            self.controls_panel.connect_buttons(self.change_to_pupk,self.change_to_pupk,self.change_to_chart)
            self.workspace = MapView()
            self.slider = Slider()
            self.window = Window(self.controls_panel,self.workspace,self.slider)
            self.window.show()
            sys.exit(self.app.exec_())
    def change_to_chart(self):
        self.window.set_workspace(self.workspace,True)
    def change_to_pupk(self):
        self.window.set_workspace(self.workspace,False)


        