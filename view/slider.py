from superqt import QLabeledRangeSlider, QLabeledSlider
from utils.names import SliderValues
from PyQt5.QtCore import Qt

class Slider(QLabeledSlider):

    def __init__(self):
        super().__init__(Qt.Horizontal)
        self.__set_ui__()
    def __set_ui__(self):

        self.setMinimum(SliderValues.MIN.value)
        self.setMaximum(SliderValues.MAX.value)

        
        self.setValue((SliderValues.SLIDER_DEFAULT_MIN.value))

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
        


class RangedSlider(QLabeledRangeSlider):

    def __init__(self):
        super().__init__()
        self.__set_ui__()
    def __set_ui__(self):

        self.setMinimum(SliderValues.MIN.value)
        self.setMaximum(SliderValues.MAX.value)

        
        self.setValue((SliderValues.SLIDER_DEFAULT_MIN.value, SliderValues.SLIDER_DEFAULT_MAX.value))

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

