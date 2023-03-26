from PyQt6 import QtWidgets, QtGui
import scipy
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

    def process(self, image):
        output_bands = self.output_band_count.value()

        # Reshape the original array into a 2D array
        height, width, depth = image.data.shape
        resampled_wavelengths = np.linspace(
            image.minimum_wavelength, image.maximum_wavelength, output_bands)

        # Create a 1D interpolation function for each row of the reshaped array
        interpolation_function_array = scipy.interpolate.interp1d(
            image.get_wavelengths(), image.data, kind=self.interpolation_selector.currentText(), axis=2)

        # Use the interpolation function to interpolate to the new axis values
        image.data = interpolation_function_array(resampled_wavelengths)

        return image
