from view.main_window import Window
from PyQt5.QtWidgets import QApplication
from model.geo_renderer import GeoRenderer
from view.controls_panel import ControlsPanel
from view.map import MapView, MapViewRegions
from view.slider import Slider, RangedSlider
from utils.file_manager import FileManager
from utils.names import ModelValues
from view.workspace import Workspace, SliderPart
from view.chart import Chart
import sys

import sys
from PyQt5.QtWidgets import QApplication



#WZORZEC MEDIATORA
class AppMediator:
    def __init__(self, file_manager, geo_renderer, workspace, slider_part, controls_panel, window, pupk_map_view, pepr_map_view, chart_pupk, chart_pepr):
        self._file_manager = file_manager
        self._geo_renderer = geo_renderer
        self._workspace = workspace
        self._slider_part = slider_part
        self._controls_panel = controls_panel
        self._window = window
        self._pupk_map_view = pupk_map_view
        self._pepr_map_view = pepr_map_view
        self._chart_pupk = chart_pupk
        self._chart_pepr = chart_pepr
        
        self._is_chart_view = False

        self._controls_panel.connect_buttons(
            self.on_pupk_button_clicked,
            self.on_pepr_button_clicked,
            self.on_chart_button_clicked
        )

    def on_pupk_button_clicked(self):
        if self._is_chart_view:
            self._window.set_workspace("chart_pupk")
            self._controls_panel.set_choosen(2)
            self._controls_panel.set_neutral(1)
            self._controls_panel.set_choosen(0)
            self._slider_part.set_workspace("chart_pupk")
        else:
            self._window.set_workspace("pupk")
            self._controls_panel.set_neutral(2)
            self._controls_panel.set_neutral(1)
            self._controls_panel.set_choosen(0)
            self._slider_part.set_workspace("pupk")

    def on_pepr_button_clicked(self):
        if self._is_chart_view:
            self._window.set_workspace("chart_pepr")
            self._controls_panel.set_choosen(2)
            self._controls_panel.set_neutral(0)
            self._controls_panel.set_choosen(1)
            self._slider_part.set_workspace("chart_pepr")
        else:
            self._window.set_workspace("pepr")
            self._controls_panel.set_neutral(2)
            self._controls_panel.set_neutral(0)
            self._controls_panel.set_choosen(1)
            self._slider_part.set_workspace("pepr")

    def on_chart_button_clicked(self):
        if not self._is_chart_view:
            self._window.set_workspace("chart_pupk")
            self._controls_panel.set_choosen(2)
            self._controls_panel.set_neutral(1)
            self._controls_panel.set_choosen(0)
            self._slider_part.set_workspace("chart_pupk")
        else:
            self._controls_panel.set_neutral(2)
            self._controls_panel.set_neutral(1)
            self._controls_panel.set_choosen(0)
            self._window.set_workspace("pupk")
            self._slider_part.set_workspace("pupk")
            
        self._is_chart_view = not self._is_chart_view

    def on_pupk_slider_changed(self, value):
        self._geo_renderer.update_for_year(value)
        self._pupk_map_view.reload()

    def on_pepr_slider_changed(self, value):
        self._geo_renderer.update_for_year_regions(value)
        self._pepr_map_view.reload()
    
    def on_chart_pupk_slider_changed(self, value):
        self._chart_pupk.set_years(value)

    def on_chart_pepr_slider_changed(self, value):
        self._chart_pepr.set_years(value)


class App:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.file_manager = FileManager()
        self.g = GeoRenderer()
        self.app = QApplication(sys.argv)
        print("Uruchomiono")
        self.controls_panel = ControlsPanel()

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
        self.slider_pepr = Slider(ModelValues.ELECTRIC_VEHICLES_RANGE_MIN.value,ModelValues.ELECTRIC_VEHICLES_RANGE_MAX.value,ModelValues.ELECTRIC_VEHICLES_DEFAULT.value)
        self.slider_chart_pupk = RangedSlider(ModelValues.END_OF_LIFE_VEHICLES_RANGE_MIN.value,ModelValues.END_OF_LIFE_VEHICLES_RANGE_MAX.value,ModelValues.END_OF_LIFE_VEHICLES_DEFAULT.value,ModelValues.END_OF_LIFE_VEHICLES_DEFAULT.value+1)
        self.slider_chart_pepr = RangedSlider(ModelValues.ELECTRIC_VEHICLES_RANGE_MIN.value,ModelValues.ELECTRIC_VEHICLES_RANGE_MAX.value,ModelValues.ELECTRIC_VEHICLES_DEFAULT.value,ModelValues.ELECTRIC_VEHICLES_DEFAULT.value+1)
        
        self.slider_part = SliderPart("pupk",self.slider_pupk)
        self.slider_part.add_workspace("pepr",self.slider_pepr)
        self.slider_part.add_workspace("chart_pupk",self.slider_chart_pupk)
        self.slider_part.add_workspace("chart_pepr",self.slider_chart_pepr)

        self.window = Window(self.controls_panel,self.workspace,self.slider_part)

        self.mediator = AppMediator(
            file_manager=self.file_manager,
            geo_renderer=self.g,
            workspace=self.workspace,
            slider_part=self.slider_part,
            controls_panel=self.controls_panel,
            window=self.window,
            pupk_map_view=self.PUPK,
            pepr_map_view=self.PEPR,
            chart_pupk=self.chart_pupk,
            chart_pepr=self.chart_pepr
        )

        self.slider_pupk.valueChanged.connect(self.mediator.on_pupk_slider_changed)
        self.slider_pepr.valueChanged.connect(self.mediator.on_pepr_slider_changed)
        self.slider_chart_pupk.valueChanged.connect(self.mediator.on_chart_pupk_slider_changed)
        self.slider_chart_pepr.valueChanged.connect(self.mediator.on_chart_pepr_slider_changed)
        
        self.window.show()
        sys.exit(self.app.exec_())