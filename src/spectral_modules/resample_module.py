from PyQt6 import QtWidgets, QtGui
import numpy as np


class SpectralResampleModule(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setToolTip("Resample image to a lower spectral resolution using linear interpolation")

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Window)

        self.label_01 = QtWidgets.QLabel("Resample image to ")
        self.output_band_count = QtWidgets.QSpinBox()
        self.output_band_count.setValue(6)
        self.output_band_count.setMinimum(2)
        self.label_02 = QtWidgets.QLabel("bands using")
        self.interpolation_selector = QtWidgets.QComboBox()
        self.interpolation_selector.addItems(
            ['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic', 'previous', 'next'])
        self.label_03 = QtWidgets.QLabel("interpolation")

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.label_01)
        self.layout.addWidget(self.output_band_count)
        self.layout.addWidget(self.label_02)
        self.layout.addWidget(self.interpolation_selector)
        self.layout.addWidget(self.label_03)

        self.layout.addStretch()
        self.layout.addWidget(self.up_button)
        self.layout.addWidget(self.down_button)
        self.layout.addWidget(self.delete_button)
        self.setLayout(self.layout)

    def process(self, spectral_image):
        output_bands = self.output_band_count.value()

        wavelengths = np.linspace(
            spectral_image.minimum_wavelength, spectral_image.maximum_wavelength, output_bands)

        spectral_image.data = spectral_image.interpolate_wavelengths(
            wavelengths, interpolation_method=self.interpolation_selector.currentText())

        return spectral_image
