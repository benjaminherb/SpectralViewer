from PyQt6 import QtWidgets
import numpy as np
import logging
from src.util.abstract_module import AbstractModule

log = logging.getLogger(__name__)


class SpectralResampleModule(AbstractModule):
    def __init__(self):
        super().__init__()

        self.setToolTip("Resample image to a lower spectral resolution using linear interpolation")

        self.label_01 = QtWidgets.QLabel("Resample image to ")
        self.output_band_count = QtWidgets.QSpinBox()
        self.output_band_count.setValue(6)
        self.output_band_count.setMinimum(2)
        self.label_02 = QtWidgets.QLabel("bands using")
        self.interpolation_selector = QtWidgets.QComboBox()
        self.interpolation_selector.addItems(
            ['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic', 'previous', 'next'])
        self.label_03 = QtWidgets.QLabel("interpolation")

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.label_01)
        self.layout.addWidget(self.output_band_count)
        self.layout.addWidget(self.label_02)
        self.layout.addWidget(self.interpolation_selector)
        self.layout.addWidget(self.label_03)

        self.layout.addStretch()
        self.layout.addLayout(self.navigation_layout)
        self.setLayout(self.layout)

    def process(self, spectral_image):
        output_bands = self.output_band_count.value()
        log.info(f"Resampling image from {spectral_image.depth()} to {output_bands} bands")

        wavelengths = np.linspace(
            spectral_image.get_minimum_wavelength(),
            spectral_image.get_maximum_wavelength(),
            output_bands)

        spectral_image.data = spectral_image.interpolate_wavelengths(
            wavelengths, interpolation_method=self.interpolation_selector.currentText())
        spectral_image.wavelengths = wavelengths

        return spectral_image
