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

        self.label_header = QtWidgets.QLabel("Change Illuminant")
        self.label_input = QtWidgets.QLabel("Input: ")
        self.input_illuminant_selector = QtWidgets.QComboBox()
        self.input_illuminant_selector.addItems(illuminants)
        self.label_output = QtWidgets.QLabel("Output: ")
        self.output_illuminant_selector = QtWidgets.QComboBox()
        self.output_illuminant_selector.addItems(illuminants)

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.header_layout = QtWidgets.QHBoxLayout()
        self.header_layout.addWidget(self.label_header)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.up_button)
        self.header_layout.addWidget(self.down_button)
        self.header_layout.addWidget(self.delete_button)

        self.input_output_layout = QtWidgets.QGridLayout()
        self.input_output_layout.addWidget(self.label_input, 0, 0)
        self.input_output_layout.addWidget(self.input_illuminant_selector, 0, 1)
        self.input_output_layout.addWidget(self.label_output, 1, 0)
        self.input_output_layout.addWidget(self.output_illuminant_selector, 1, 1)
        self.input_output_layout.setColumnStretch(self.input_output_layout.columnCount(), 1)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.header_layout)
        self.layout.addLayout(self.input_output_layout)

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
