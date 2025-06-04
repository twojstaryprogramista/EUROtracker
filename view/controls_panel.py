from PyQt5.QtWidgets import QWidget,QHBoxLayout, QPushButton
from utils.names import Style

class ControlsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()
        #self.button1.onclick.connect()
    def set_ui(self):
        self.layout = QHBoxLayout()

        button1 = QPushButton("P. U. P. K.")
        button1.setMinimumHeight(40)
        button1.setStyleSheet(f"""
        QPushButton {{
            background-color: {Style.BUTTON_COLOR.value};       /* niebieski */
            color: white;                    /* biały tekst */
            font-weight: bold;               /* gruba czcionka */
            border: none;                    /* brak obwódki */
            padding: 10px;                   /* wewnętrzny margines */
        }}
        QPushButton:hover {{
            background-color: #0056b3;       /* ciemniejszy niebieski po najechaniu */
        }}
        """)
        self.button1 = button1
        self.layout.addWidget(button1)

        button2 = QPushButton("P. E. P. R.")
        button2.setMinimumHeight(40)
        self.button2 = button2
        button2.setStyleSheet(f"""
        QPushButton {{
            background-color: {Style.BUTTON_COLOR.value};       /* niebieski */
            color: white;                    /* biały tekst */
            font-weight: bold;               /* gruba czcionka */
            border: none;                    /* brak obwódki */
            padding: 10px;                   /* wewnętrzny margines */
        }}
        QPushButton:hover {{
            background-color: #0056b3;       /* ciemniejszy niebieski po najechaniu */
        }}
        """)
        self.layout.addWidget(button2)



        button3 = QPushButton("Wykres")
        button3.setMinimumHeight(40)
        self.button3 = button3
        button3.setStyleSheet(f"""
        QPushButton {{
            background-color: {Style.BUTTON_COLOR.value};       /* niebieski */
            color: white;                    /* biały tekst */
            font-weight: bold;               /* gruba czcionka */
            border: none;                    /* brak obwódki */
            padding: 10px;                   /* wewnętrzny margines */
        }}
        QPushButton:hover {{
            background-color: #0056b3;       /* ciemniejszy niebieski po najechaniu */
        }}
        """)
        self.layout.addWidget(button3)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

    def connect_buttons(self,f1,f2,f3):
        self.button1.clicked.connect(f1)
        self.button2.clicked.connect(f2)
        self.button3.clicked.connect(f3)
