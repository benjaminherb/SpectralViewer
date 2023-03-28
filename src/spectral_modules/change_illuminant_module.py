from PyQt6 import QtWidgets, QtGui
import scipy
import numpy as np
from src.data_loader.load_illuminants import load_illuminant


class ChangeIlluminantModule(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setToolTip("Change illuminant")

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Window)

        self.label_01 = QtWidgets.QLabel("Change illuminant from")
        self.input_illuminant_selector = QtWidgets.QComboBox()
        self.input_illuminant_selector.addItems(['CIE D65', 'CIE D50', 'CIE A'])
        self.label_02 = QtWidgets.QLabel("to")
        self.output_illuminant_selector = QtWidgets.QComboBox()
        self.output_illuminant_selector.addItems(['CIE D65', 'CIE D50', 'CIE A'])

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.label_01)
        self.layout.addWidget(self.input_illuminant_selector)
        self.layout.addWidget(self.label_02)
        self.layout.addWidget(self.output_illuminant_selector)

        self.layout.addStretch()
        self.layout.addWidget(self.up_button)
        self.layout.addWidget(self.down_button)
        self.layout.addWidget(self.delete_button)
        self.setLayout(self.layout)

    def process(self, spectral_image):
        wavelengths = spectral_image.get_wavelengths()

        input_illuminant = load_illuminant(
            self.input_illuminant_selector.currentText(), wavelengths)
        output_illuminant = load_illuminant(
            self.output_illuminant_selector.currentText(), wavelengths)

        spectral_image.data = spectral_image.data / input_illuminant
        spectral_image.data = spectral_image.data * output_illuminant

        return spectral_image
