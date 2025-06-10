from view.chart import get_names,get_values,Chart,ChartControlPanel
from PyQt5.QtWidgets import QApplication
import sys
from utils.file_manager import FileManager


if __name__ =="__main__":
    names = get_names()
    values = get_values(names)
    application = QApplication(sys.argv)
    #control_panel = ChartControlPanel(names)
    f = FileManager()
    chart = Chart(f,False)
    chart.show()
    sys.exit(application.exec())