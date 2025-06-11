from superqt import QLabeledRangeSlider, QLabeledSlider
from PyQt5.QtCore import Qt

class Slider(QLabeledSlider):

    def __init__(self,min,max,default):
        super().__init__(Qt.Horizontal)
        self.min = min
        self.max = max
        self.default = default
        self.__set_ui__()


    def __set_ui__(self):

        #self.setMinimum(SliderValues.MIN.value)
        #self.setMaximum(SliderValues.MAX.value)
        self.setMinimum(self.min)
        self.setMaximum(self.max)
        self.setValue(self.default)

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

    def __init__(self,min,max,default_min,default_max):
        super().__init__()
        self.min = min
        self.max = max
        self.default_min = default_min
        self.default_max = default_max
        self.__set_ui__()

    def __set_ui__(self):

        self.setMinimum(self.min)
        self.setMaximum(self.max)

        
        self.setValue([self.default_min,self.default_max])

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

