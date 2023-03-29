from PyQt6 import QtWidgets, QtGui, QtCore
import numpy as np
from src.data_loader.load_illuminants import load_illuminant


class SaturationModule(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setToolTip("Change saturation")

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Window)

        self.label_01 = QtWidgets.QLabel("Illuminant")
        self.illuminant_selector = QtWidgets.QComboBox()
        self.illuminant_selector.addItems(['None', 'CIE D65'])

        self.label_02 = QtWidgets.QLabel("Saturation")
        self.saturation_slider = QtWidgets.QSlider()
        self.saturation_value_label = QtWidgets.QLabel()
        self.saturation_value_label.setMinimumWidth(60)

        self.saturation_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.saturation_slider.valueChanged.connect(self._update_saturation_label)
        self.saturation_slider.setMinimum(000)
        self.saturation_slider.setMaximum(1000)
        self.saturation_slider.setValue(100)

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.label_01, 0, 0)
        self.layout.addWidget(self.illuminant_selector, 0, 1)
        self.layout.addWidget(self.label_02, 1, 0)
        self.layout.addWidget(self.saturation_slider, 1, 1)
        self.layout.addWidget(self.saturation_value_label, 1, 2)

        self.layout.addWidget(self.up_button, 0, 3)
        self.layout.addWidget(self.down_button, 0, 4)
        self.layout.addWidget(self.delete_button, 0, 5)
        self.setLayout(self.layout)

    def process(self, spectral_image):
        saturation = _map_value_to_saturation(self.saturation_slider.value())
        illuminant = None
        if self.illuminant_selector.currentText() != "None":
            illuminant = load_illuminant(self.illuminant_selector.currentText(),
                                         spectral_image.get_wavelengths())

        if illuminant is not None:
            spectral_image.data = spectral_image.data / illuminant

        max_values = np.max(spectral_image.data, axis=2, keepdims=True)
        spectral_image.data = np.power(spectral_image.data / max_values, saturation) * max_values

        if illuminant is not None:
            spectral_image.data = spectral_image.data * illuminant

        return spectral_image

    def _update_saturation_label(self, value):
        self.saturation_value_label.setText(f"{_map_value_to_saturation(value):.2f}")


def _map_value_to_saturation(value):
    return value / 100
