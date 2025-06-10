import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.colors as mcolors


class ChartArea(QWidget):

    def __init__(self,file_manager,years,is_pupk):
        super().__init__()



        self.setWindowTitle("Wieloroczne wykresy słupkowe")
        self.setGeometry(100, 100, 1000, 600)

        layout = QVBoxLayout()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.legend  =QWidget()
        self.legend_layout=QHBoxLayout()

        self.legend.setLayout(self.legend_layout)
        layout.addWidget(self.canvas)
        layout.addWidget(self.legend)
        self.setLayout(layout)
        self.file_manager = file_manager
        self.years = years
        if is_pupk:
            self.values = [self.file_manager.value_organizer.get_values_for_year_countries(year) for year in self.years]
        else:
            self.values = [self.file_manager.value_organizer.get_values_for_year_regions(year) for year in self.years]


        self.countries = self.file_manager.get_countries() if is_pupk else self.file_manager.get_regions()
        self.legend_labels = []

        available_colors = list(mcolors.TABLEAU_COLORS.values())

        self.colors = {
            country: available_colors[i % len(available_colors)]
            for i, country in enumerate(self.countries)
        }

        for i in range(len(self.countries)):
            name = self.countries[i]
            label = LegendLabel(self.colors[name],name)
            self.legend_layout.addWidget(label)
            self.legend_labels.append(label)
            label.setVisible(False)

        #self.plot_multiple_bar_charts(self.file_manager.get_countries(),[self.file_manager.value_organizer.get_values_for_year_countries(2021),self.file_manager.value_organizer.get_values_for_year_countries(2022)],[2021,2022])
        #self.filter_bars(['Poland','Norway','Germany','Belgium'],[2019,2020,2021,2022])

    #def filter_bars(self,list,years)
    def save_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self,"Zapisz jako PDF","","PDF Files (*.pdf)")
        if path:
            #self.figure.tight_layout()
            self.figure.savefig(path,format='pdf')

    def filter_bars(self,list,years):
        for country in self.countries:
            index = self.countries.index(country)
            self.legend_labels[index].setVisible(False)
        new_values =[]
        for year in years:
            index = self.years.index(year)
            new_values.append(self.values[index])
        values = new_values
        new_values =[]
        for i, year in enumerate(values):
            new_year = []
            for country in self.countries:
                if country in list:
                    index = self.countries.index(country)
                    new_year.append(values[i][index])
                    self.legend_labels[index].setVisible(True)
            new_values.append(new_year)
        self.plot_multiple_bar_charts(list,new_values,years)

    def plot_multiple_bar_charts(self,countries,values,years):
        self.figure.clear()
        # Dane przykładowe
        #countries = ['Mazowieckie', 'Śląskie', 'Wielkopolskie', 'Pomorskie']
        lata = years

        # Losowe dane
        #all_values = [
        #    [random.randint(100, 600) for _ in countries]
        #    for _ in lata
        #]

        # Kolory dla regionów
        #colors = {
        #    region: color for region, color in zip(
        #        countries,
        #        ["#ff0000", "#00ff00", '#bb00ff', "#0000ff"]
        #    )
        #}
        available_colors = list(mcolors.TABLEAU_COLORS.values())

        colors = {
            country: available_colors[i % len(available_colors)]
            for i, country in enumerate(countries)
        }
        # Tworzymy subplota dla każdego roku
        cols = len(lata)

        for i,year in enumerate(years):
            ax = self.figure.add_subplot(1, cols, i + 1)
            bars = ax.bar(
                x = range(len(countries)),
                height =values[i],
                color=[self.colors[region] for region in countries],
                width=0.7
            )
        

            # Ukrywamy wszystko zbędne
            ax.set_xticks([])
            #ax.set_ylim(0, max(values))
            if i > 0: ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)
            # Podpisujemy rok pod wykresem
            #ax.set_ylabel('Wartość')

# Opcjonalnie: ustawienie zakresu osi 
            ax.set_xlabel(str(year), labelpad=10)



        self.canvas.draw()

class LegendLabel(QWidget):
    def __init__(self,color,label):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.addWidget(CircleWidget(color,10))
        self.layout.addWidget(QLabel(label))
        self.setLayout(self.layout)



class CircleWidget(QWidget):
    def __init__(self, color=Qt.red, diameter=30, parent=None):
        super().__init__(parent)
        self.color = QColor(color)
        self.diameter = diameter
        self.setFixedSize(diameter, diameter)  # rozmiar widgetu = średnica kółka

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # gładkie krawędzie
        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)  # bez obramowania
        painter.drawEllipse(0, 0, self.diameter, self.diameter)  # rysuj koło

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChartArea()
    window.show()
    sys.exit(app.exec())
