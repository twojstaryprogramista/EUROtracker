from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy

from utils.names import WindowValues
from PyQt5.QtCore import Qt


class Window(QWidget):
    def __init__(self,controls_panel,workspace,slider):
        super().__init__()
        self.regions_map = None
        self._current_spacer=None
        self.controls_panel = controls_panel
        self.workspace = workspace
        self.slider = slider
        self.set_ui()
    def set_ui(self):
        self.set_window()
        self.set_content()






    def set_window(self):
        self.setWindowTitle(WindowValues.APP_NAME.value)
        self.setWindowFlags(Qt.Window |
                    Qt.WindowTitleHint |
                    Qt.WindowMinimizeButtonHint |
                    Qt.WindowCloseButtonHint)

        self.setFixedSize(WindowValues.WIDTH.value, WindowValues.HEIGHT.value)
    def set_content(self):
        self.layout = QVBoxLayout()
        
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.controls_panel)
        self.layout.addWidget(self.workspace)
        self.layout.addWidget(self.slider)
        self.layout.addSpacing(20)

        self.setLayout(self.layout)

    def set_workspace(self,name):
        self.workspace.set_workspace(name)
        self.slider.set_workspace(name)
    def set_workspaceold(self,workspace,remove):
        if remove == True:
            if self._current_spacer==None:
                if self.regions_map is not None:
                    self.regions_map.setParent(None)
                self.workspace.setParent(None)
                
                spacer = QSpacerItem(0, 480, QSizePolicy.Minimum, QSizePolicy.Fixed)  # wysokość 100px

                self.layout.insertSpacerItem(1, spacer)  # na miejsce 1 (tam gdzie był widget)

                self._current_spacer = spacer
        else:
            if self.regions_map is not None:
                self.regions_map.setParent(None)
            self.layout.removeItem(self._current_spacer)
            self._current_spacer=None
            self.layout.insertWidget(1,self.workspace)
    def set_pepr(self, regions_map):
        self.layout.removeItem(self._current_spacer)
        self._current_spacer=None
        self.regions_map = regions_map
        self.workspace.setParent(None)
        self.layout.insertWidget(1,self.regions_map)
        print("PEPR")