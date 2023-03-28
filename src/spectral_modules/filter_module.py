from PyQt6 import QtWidgets, QtGui
import numpy as np
from src.data_loader.load_filters import load_filter


class FilterModule(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setToolTip("Apply color filters")

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Window)

        self.label_01 = QtWidgets.QLabel("Apply")
        self.filter_selector = QtWidgets.QComboBox()
        self.filter_selector.addItems(
            ["Rose Pink", "Lavender Tint", "Medium Bastard Amber", "Pale Yellow",
             "Dark Salmon", "Pale Amber Gold", "Medium Yellow", "Straw Tint",
             "Deep Straw", "Surprise Peach", "Fire", "Medium Amber", "Gold Amber",
             "Dark Amber", "Scarlet", "Sunset Red", "Bright Red", "Medium Red",
             "Plasa Red", "Light Pink", "Medium Pink", "Pink Carnation", "Dark Magenta",
             "Rose Purple", "Light Lavender", "Paler Lavender", "Lavender", "Mist Blue",
             "Pale Blue", "Sky Blue"])

        self.label_02 = QtWidgets.QLabel("filter")

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.label_01)
        self.layout.addWidget(self.filter_selector)
        self.layout.addWidget(self.label_02)

        self.layout.addStretch()
        self.layout.addWidget(self.up_button)
        self.layout.addWidget(self.down_button)
        self.layout.addWidget(self.delete_button)
        self.setLayout(self.layout)

    def process(self, spectral_image):
        filter = load_filter(self.filter_selector.currentText(), spectral_image.get_wavelengths())

        spectral_image.data = spectral_image.data * filter

        return spectral_image
