from PyQt6 import QtWidgets, QtCore


class ControlWidget(QtWidgets.QWidget):
    update_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QGridLayout()

        # band selector
        self.band_selector_layout = QtWidgets.QHBoxLayout()
        self.band0 = QtWidgets.QSpinBox()
        self.band0.setValue(20)
        self.band1 = QtWidgets.QSpinBox()
        self.band1.setValue(13)
        self.band2 = QtWidgets.QSpinBox()
        self.band2.setValue(5)
        self.band_selector_layout.addWidget(self.band0)
        self.band_selector_layout.addWidget(self.band1)
        self.band_selector_layout.addWidget(self.band2)
        self.band_selector = QtWidgets.QWidget()
        self.band_selector.setLayout(self.band_selector_layout)

        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self.refresh_button.pressed.connect(self.update_signal)
        self.layout.addWidget(self.band_selector, 0, 0)
        self.layout.addWidget(self.refresh_button, 1, 0)

        self.setLayout(self.layout)

    def get_bands(self):
        return self.band0.value(), self.band1.value(), self.band2.value()
