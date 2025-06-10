from view.main_window import Window
from PyQt5.QtWidgets import QApplication, QWidget
from model.geo_renderer import GeoRenderer
from view.controls_panel import ControlsPanel
from view.map import MapView, MapViewRegions
from view.slider import Slider, RangedSlider
from utils.file_manager import FileManager
from utils.names import ModelValues
from view.workspace import Workspace, SliderPart
from view.chart import Chart
import sys
from PyQt5.QtWidgets import QSlider

class App:


    _instance = None


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
            
            self.file_manager = FileManager()
            self.g = GeoRenderer(self.file_manager)
            self.app = QApplication(sys.argv)
            print("Uruchomiono")
            self.controls_panel = ControlsPanel()
            self.controls_panel.connect_buttons(self.change_to_pupk,self.change_to_pepr,self.change_to_chart)


            self.PUPK = MapView()
            self.is_chart = False
            self.workspace = Workspace("pupk",self.PUPK)
            self.PEPR = MapViewRegions()
            self.workspace.add_workspace("pepr",self.PEPR)
            self.chart_pupk = Chart(self.file_manager,True)
            self.workspace.add_workspace("chart_pupk",self.chart_pupk)
            self.chart_pepr = Chart(self.file_manager,False)
            self.workspace.add_workspace("chart_pepr",self.chart_pepr)


            self.slider_pupk = Slider(ModelValues.END_OF_LIFE_VEHICLES_RANGE_MIN.value,ModelValues.END_OF_LIFE_VEHICLES_RANGE_MAX.value,ModelValues.END_OF_LIFE_VEHICLES_DEFAULT.value)
            self.slider_pupk.valueChanged.connect(lambda value: (self.g.update_for_year(value), self.PUPK.reload()))

            self.slider_pepr = Slider(ModelValues.ELECTRIC_VEHICLES_RANGE_MIN.value,ModelValues.ELECTRIC_VEHICLES_RANGE_MAX.value,ModelValues.ELECTRIC_VEHICLES_DEFAULT.value)
            self.slider_pepr.valueChanged.connect(lambda value: (self.handle_pepr(value)))

            self.slider_chart_pupk = RangedSlider(ModelValues.END_OF_LIFE_VEHICLES_RANGE_MIN.value,ModelValues.END_OF_LIFE_VEHICLES_RANGE_MAX.value,ModelValues.END_OF_LIFE_VEHICLES_DEFAULT.value,ModelValues.END_OF_LIFE_VEHICLES_DEFAULT.value+1)
            self.slider_chart_pupk.valueChanged.connect(lambda value: (self.chart_pupk.set_years(value)))

            self.slider_chart_pepr = RangedSlider(ModelValues.ELECTRIC_VEHICLES_RANGE_MIN.value,ModelValues.ELECTRIC_VEHICLES_RANGE_MAX.value,ModelValues.ELECTRIC_VEHICLES_DEFAULT.value,ModelValues.ELECTRIC_VEHICLES_DEFAULT.value+1)
            self.slider_chart_pepr.valueChanged.connect(lambda value: (self.chart_pepr.set_years(value)))
            #self.slider.valueChanged.connect(lambda value: (self.g.set_values(value), self.workspace.reload()))
            
            #self.slider.valueChanged.connect(lambda value: (self.g.update_for_year_regions(value), self.workspace.get_current_workspace().reload()))
            self.slider_part = SliderPart("pupk",self.slider_pupk)
            self.slider_part.add_workspace("pepr",self.slider_pepr)
            self.slider_part.add_workspace("chart_pupk",self.slider_chart_pupk)#chart_pupk
            self.slider_part.add_workspace("chart_pepr",self.slider_chart_pepr)
            #self.slider_part.set_workspace("pupk")

            self.window = Window(self.controls_panel,self.workspace,self.slider_part)
            
            self.window.show()
            sys.exit(self.app.exec_())
    def change_to_chart(self):
        if not self.is_chart:
            self.window.set_workspace("chart_pupk")
            self.controls_panel.set_choosen(2)
            self.controls_panel.set_neutral(1)
            self.controls_panel.set_choosen(0)
        else:
            self.controls_panel.set_neutral(2)
            self.controls_panel.set_neutral(1)
            self.controls_panel.set_choosen(0)
            self.window.set_workspace("pupk")
             
        self.is_chart = not (self.is_chart)
    def change_to_pupk(self):
        if self.is_chart:
            self.controls_panel.set_choosen(2)
            self.controls_panel.set_neutral(1)
            self.controls_panel.set_choosen(0)
            self.window.set_workspace("chart_pupk")
        else:
            self.window.set_workspace("pupk")
            self.controls_panel.set_neutral(2)
            self.controls_panel.set_neutral(1)
            self.controls_panel.set_choosen(0)
    def change_to_pepr(self):
        if self.is_chart:
            self.window.set_workspace("chart_pepr")
            self.controls_panel.set_choosen(2)
            self.controls_panel.set_neutral(0)
            self.controls_panel.set_choosen(1)
        else:
            self.window.set_workspace("pepr")
            self.controls_panel.set_neutral(2)
            self.controls_panel.set_neutral(0)
            self.controls_panel.set_choosen(1)
    def handle_pepr(self,value):
         self.g.update_for_year_regions(value)
         self.PEPR.reload()
    def handle_pupk(self,value):
        self.g.update_for_year(value)
        self.PEPR.reload()


        