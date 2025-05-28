from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from utils.names import WindowValues
from view.controls_panel import ControlsPanel

# Utworzenie aplikacji

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.set_ui()

        # Pokazanie okna
    def set_ui(self):
        self.setWindowTitle(WindowValues.APP_NAME.value)
        self.setGeometry(100, 100, 400, 300)  # (x, y, szerokość, wysokość)

        self.controls_panel = ControlsPanel()
        self.workspace = QWidget()
        self.slider = QWidget()


        self.layout = QVBoxLayout()
        
        self.layout.setSpacing(0)        # odstęp między widgetami = 0
        self.layout.setContentsMargins(0, 0, 0, 0)  # marginesy wewnątrz layoutu = 0
        self.layout.addWidget(self.controls_panel)
        self.layout.addWidget(self.workspace)
        self.layout.addWidget(self.slider)



        self.setLayout(self.layout)
#window = Window()

