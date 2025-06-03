from superqt import QLabeledRangeSlider
from PyQt5.QtGui import QColor


class Slider(QLabeledRangeSlider):
    def __init__(self):
        super().__init__()
        self.__set_ui__()
    def __set_ui__(self):

        self.setMinimum(2001)
        self.setMaximum(2025)

        # Aktualny zakres wybrany przez użytkownika (np. 20–80)
        self.setValue((2010, 2013))  # lub slider.setRange(20, 80)

        self.setStyleSheet("""
QSlider::groove:horizontal {
    height: 6px;
    background: #d0d0d0;
    border-radius: 3px;
}

QSlider::sub-page:horizontal {
    background: #007aff;  /* NIEBIESKI pasek między */
    border-radius: 3px;
}



QSlider::handle:horizontal {
    background: white;
    border: 1px solid #888;
    width: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QRangeSlider {
    qproperty-barColor: #007aff;
}
""")
