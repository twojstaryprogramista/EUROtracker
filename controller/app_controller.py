from view.main_window import Window
from PyQt5.QtWidgets import QApplication
import sys

class App:
    def __init__(self):
        app = QApplication(sys.argv)
        window = Window()

        # Utworzenie głównego okna
        window.show()

        # Uruchomienie pętli aplikacji
        sys.exit(app.exec_())

        