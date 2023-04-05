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

        self.convert_label = QtWidgets.QLabel("Convert")
        self.input_selector = QtWidgets.QComboBox()
        self.input_selector.addItems(get_illuminant_names())
        self.to_label = QtWidgets.QLabel("to")
        self.output_selector = QtWidgets.QComboBox()
        self.output_selector.addItems(get_illuminant_names())

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.convert_label)
        self.layout.addWidget(self.input_selector)
        self.layout.addWidget(self.to_label)
        self.layout.addWidget(self.output_selector)
        self.layout.addStretch()
        self.layout.addWidget(self.up_button)
        self.layout.addWidget(self.down_button)
        self.layout.addWidget(self.delete_button)
        self.setLayout(self.layout)

    def process(self, image):
        XYZ_image = RGB_to_XYZ(image)
        XYZ_image = chromatic_adaptation(
            XYZ_image, self.input_selector.currentText(), self.output_selector.currentText())
        RGB_image = XYZ_to_RGB(XYZ_image)
        return RGB_image
