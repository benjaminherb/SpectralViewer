from PyQt6 import QtWidgets, QtGui
import logging
from src.data_loader.load_illuminants import load_illuminant, get_illuminant_names

log = logging.getLogger(__name__)


class ChangeIlluminantModule(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setToolTip("Change illuminant")

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Window)

        illuminants = get_illuminant_names()

        self.label_input = QtWidgets.QLabel("Input Illuminant: ")
        self.input_illuminant_selector = QtWidgets.QComboBox()
        self.input_illuminant_selector.addItems(illuminants)
        self.label_output = QtWidgets.QLabel("Output Illuminant: ")
        self.output_illuminant_selector = QtWidgets.QComboBox()
        self.output_illuminant_selector.addItems(illuminants)

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.label_input, 0, 0)
        self.layout.addWidget(self.input_illuminant_selector, 0, 1)
        self.layout.addWidget(self.label_output, 1, 0)
        self.layout.addWidget(self.output_illuminant_selector, 1, 1)
        self.layout.setColumnStretch(2, 2)
        self.layout.addWidget(self.up_button, 0, 3)
        self.layout.addWidget(self.down_button, 0, 4)
        self.layout.addWidget(self.delete_button, 0, 5)

        self.setLayout(self.layout)

    def process(self, spectral_image):
        wavelengths = spectral_image.get_wavelengths()

        input_illuminant = load_illuminant(
            self.input_illuminant_selector.currentText(), wavelengths)
        output_illuminant = load_illuminant(
            self.output_illuminant_selector.currentText(), wavelengths)

        log.info(f"Changing illuminant from {self.input_illuminant_selector.currentText()} "
                 f"to {self.output_illuminant_selector.currentText()}")

        spectral_image.data = spectral_image.data / input_illuminant
        spectral_image.data = spectral_image.data * output_illuminant

        return spectral_image
