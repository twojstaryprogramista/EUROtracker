import ast
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QScrollArea, QSizePolicy, QHBoxLayout, QLineEdit
import random
from view.plot import ChartArea
from utils.file_manager import FileManager

def get_values(names):
    rok_start = 2021
    rok_koniec = 2024
    min_wartosc = 100
    max_wartosc = 600

    dane = []

    for rok in range(rok_start, rok_koniec + 1):
        wartosci = [random.randint(min_wartosc, max_wartosc) for _ in names]
        dane.append(wartosci)
    #for i, rok in enumerate(range(rok_start, rok_koniec + 1)):
    #    print(f"{rok}: {dane[i]}\n\n")
    #print(dane)
    return dane
    
def get_names():
    s = "['France', 'Ukraine', 'Belarus', 'Lithuania', 'Russia', 'Czechia', 'Germany', 'Estonia', 'Latvia', 'Norway', 'Sweden', 'Finland', 'Luxembourg', 'Belgium', 'North Macedonia', 'Albania', 'Kosovo', 'Spain', 'Denmark', 'Romania', 'Hungary', 'Slovakia', 'Poland', 'Ireland', 'United Kingdom', 'Greece', 'Austria', 'Italy', 'Switzerland', 'Netherlands', 'Liechtenstein', 'Serbia', 'Croatia', 'Slovenia', 'Bulgaria', 'San Marino', 'Monaco', 'Andorra', 'Montenegro', 'Bosnia and Herz.', 'Portugal', 'Moldova', 'Gibraltar', 'Vatican', 'Iceland', 'Malta', 'Jersey', 'Guernsey', 'Isle of Man', 'Åland', 'Faeroe Is.']"
    lista = ast.literal_eval(s)
    return lista

class SpacelessVBoxLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
class SpacelessHBoxLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


class Chart(QWidget):
    def __init__(self,file_manager,is_pupk):
        super().__init__()
        self.file_manager = FileManager()
        
        if is_pupk:
            self.years = self.file_manager.get_years_countries()
            self.names = self.file_manager.get_country_names()
        else:
            self.years = self.file_manager.get_years_regions()
            self.names = self.file_manager.get_region_names()
        self.chart_area = ChartArea(self.file_manager,self.years,is_pupk)
        self.control_panel = ChartControlPanel(self.names,self.chart_area)
        self.__set_ui__()
    def __set_ui__(self):
        self.layout = SpacelessHBoxLayout()
        self.layout.addWidget(self.chart_area)
        self.layout.addWidget(self.control_panel)
        self.setLayout(self.layout)
        
    def set_years(self,min_max):
        self.control_panel.set_years(min_max)

    def set_save_pdf_action(self,function):
        self.control_panel.set_save_pdf_action(function)


class ChartControlPanel(QWidget):
    def __init__(self,names,chart_area):

        szukanie = "Znajdź kraj..."
        self.chart_countries = []
        self.chart_area = chart_area
        super().__init__()
        self.names = names
        self.setWindowTitle("Scrollowalna lista przycisków")
        self.resize(300, 400)
        self.buttons =[]
        self.years = [2020,2021,2022]
        scroll = QScrollArea()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(szukanie)
        self.search_box.textChanged.connect(lambda text: (self.update_list(text)))
        scroll.setWidgetResizable(True)

        content = QWidget()
        self.layout = SpacelessVBoxLayout()

        content.setLayout(self.layout)
        for i in range(len(names)):
            button = QPushButton(f"{names[i]}")
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.addWidget(button)
            self.buttons.append(button)
            button.clicked.connect(lambda _, name=names[i]: self.update_chart_countries(name))
            self.set_neutral(i)
        scroll.setWidget(content)

        self.save_pdf = QPushButton("Zapisz do PDF")
        self.save_pdf.setStyleSheet(f"""
        QPushButton {{
            background-color: #bbbbbb;       /* niebieski */
            color: black;                    /* biały tekst */
            font-weight: bold;               /* gruba czcionka */
            border: 1px solid black;                    /* brak obwódki */
            padding: 5px;                   /* wewnętrzny margines */
        }}
        QPushButton:hover {{
            background-color: #999999;       /* ciemniejszy niebieski po najechaniu */
        }}
        """)
        self.main_layout = SpacelessVBoxLayout()
        self.main_layout.addWidget(self.search_box)
        self.main_layout.addWidget(scroll)
        self.main_layout.addWidget(self.save_pdf)
        self.setLayout(self.main_layout)
        self.set_save_pdf_action(self.chart_area.save_pdf)
    def set_neutral(self,index):
        self.buttons[index].setStyleSheet(f"""
        QPushButton {{
            background-color: #bbbbbb;       /* niebieski */
            color: black;                    /* biały tekst */
            font-weight: bold;               /* gruba czcionka */
            border: 1px solid black;                    /* brak obwódki */
            padding: 5px;                   /* wewnętrzny margines */
        }}
        QPushButton:hover {{
            background-color: #999999;       /* ciemniejszy niebieski po najechaniu */
        }}
        """)
    def set_choosen(self,index):
        self.buttons[index].setStyleSheet(f"""
        QPushButton {{
            background-color: #999999;       /* niebieski */
            color: black;                    /* biały tekst */
            font-weight: bold;               /* gruba czcionka */
            border: 1px solid black;                    /* brak obwódki */
            padding: 5px;                    /* wewnętrzny margines */
        }}
        QPushButton:hover {{
            background-color: #777777;       /* ciemniejszy niebieski po najechaniu */
        }}
        """)
    def update_chart_countries(self,name):
        if name not in self.chart_countries:
            if len(self.chart_countries)<5:
                index = self.names.index(name)
                self.set_choosen(index)
                self.chart_countries.append(name)
                self.chart_area.filter_bars(self.chart_countries,self.years)
        else:
            index = self.names.index(name)
            self.chart_countries.remove(name)
            self.set_neutral(index)
            self.chart_area.filter_bars(self.chart_countries,self.years)
    def set_years(self,min_max):
        self.years = list(range(min_max[0],min_max[1]+1))
        self.chart_area.filter_bars(self.chart_countries,self.years)

    def update_list(self,text):
        if text:
            for name, button in zip(self.names, self.buttons):
                if text.lower() in name.lower():
                    button.show()
                else:
                    button.hide()
        else:
            for button in self.buttons:
                button.show()

    def set_button_action(self,name,function):
        index = self.names.index(name)
        self.buttons[index].clicked.connect(function)
    def set_save_pdf_action(self,function):
        self.save_pdf.clicked.connect(function)

if __name__ =="__main__":
    names = get_names()
    values = get_values(names)
    application = QApplication(sys.argv)
    control_panel = ChartControlPanel(names)
    chart = Chart(names, values)
    chart.show()
    sys.exit(application.exec())
