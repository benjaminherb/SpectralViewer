from PyQt6 import QtWidgets, QtGui, QtCore
import numpy as np
import logging
from src.data_loader.load_illuminants import load_illuminant, get_illuminant_names
from src.util.abstract_module import AbstractModule

log = logging.getLogger(__name__)


class SaturationModule(AbstractModule):
    def __init__(self):
        super().__init__()

        self.setToolTip("Change saturation")

        self.label_01 = QtWidgets.QLabel("Illuminant")
        self.illuminant_selector = QtWidgets.QComboBox()
        illuminants = ['None']
        illuminants.extend(get_illuminant_names())
        self.illuminant_selector.addItems(illuminants)

        self.label_02 = QtWidgets.QLabel("Saturation")
        self.saturation_slider = QtWidgets.QSlider()
        self.saturation_value_label = QtWidgets.QLabel()
        self.saturation_value_label.setMinimumWidth(60)

        self.saturation_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.saturation_slider.valueChanged.connect(self._update_saturation_label)
        self.saturation_slider.setMinimum(000)
        self.saturation_slider.setMaximum(1000)
        self.saturation_slider.setValue(100)

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.label_01, 0, 0)
        self.layout.addWidget(self.illuminant_selector, 0, 1)
        self.layout.addWidget(self.label_02, 1, 0)
        self.layout.addWidget(self.saturation_slider, 1, 1)
        self.layout.addWidget(self.saturation_value_label, 1, 2)

        self.layout.addLayout(self.navigation_layout, 0,3)
        self.setLayout(self.layout)

    def process(self, spectral_image):
        saturation = _map_value_to_saturation(self.saturation_slider.value())
        log.info(f"Applying {saturation:.2f} saturation "
                 f"with illuminant {self.illuminant_selector.currentText()}")

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
