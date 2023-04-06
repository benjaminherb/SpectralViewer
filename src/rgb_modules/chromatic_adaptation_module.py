from PyQt6 import QtWidgets, QtGui
import logging
from src.data_loader.load_illuminants import get_illuminant_names
from src.conversions.tristimulus import chromatic_adaptation
from src.conversions.tristimulus import XYZ_to_RGB, RGB_to_XYZ

log = logging.getLogger(__name__)


class ChromaticAdaptationModule(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setToolTip("Chromatic Adaptation")

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Window)

        self.input_label = QtWidgets.QLabel("Input Illuminant:")
        self.input_selector = QtWidgets.QComboBox()
        self.input_selector.addItems(get_illuminant_names())
        self.output_label = QtWidgets.QLabel("Output Illuminant:")
        self.output_selector = QtWidgets.QComboBox()
        self.output_selector.addItems(get_illuminant_names())
        self.method_label = QtWidgets.QLabel("Method")
        self.method_selector = QtWidgets.QComboBox()
        self.method_selector.addItems(["Bradford", "Von Kries", "XYZ"])

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.input_label, 0, 0)
        self.layout.addWidget(self.input_selector, 0, 1)
        self.layout.addWidget(self.output_label, 1, 0)
        self.layout.addWidget(self.output_selector, 1, 1)
        self.layout.addWidget(self.method_label, 2, 0)
        self.layout.addWidget(self.method_selector, 2, 1)
        self.layout.setColumnStretch(2, 2)
        self.layout.addWidget(self.up_button, 0, 3)
        self.layout.addWidget(self.down_button, 0, 4)
        self.layout.addWidget(self.delete_button, 0, 5)
        self.setLayout(self.layout)

    def process(self, image):
        input = self.input_selector.currentText()
        output = self.output_selector.currentText()
        method = self.method_selector.currentText()

        log.info(f"Chromatic adaptation from {input} to {output} using {method}")

        XYZ_image = RGB_to_XYZ(image)
        XYZ_image = chromatic_adaptation(XYZ_image, input, output, method)
        RGB_image = XYZ_to_RGB(XYZ_image)

        return RGB_image
