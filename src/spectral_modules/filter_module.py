from PyQt6 import QtWidgets, QtGui
import logging
from src.data_loader.load_filters import load_filter, get_filter_names
from src.util.abstract_module import AbstractModule

log = logging.getLogger(__name__)


class FilterModule(AbstractModule):
    def __init__(self):
        super().__init__()

        self.setToolTip("Apply color filters")

        self.label_01 = QtWidgets.QLabel("Apply")
        self.filter_selector = QtWidgets.QComboBox()
        self.filter_selector.addItems(get_filter_names())
        self.label_02 = QtWidgets.QLabel("filter")

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.label_01)
        self.layout.addWidget(self.filter_selector)
        self.layout.addWidget(self.label_02)

        self.layout.addStretch()
        self.layout.addLayout(self.navigation_layout)
        self.setLayout(self.layout)

    def process(self, spectral_image):
        log.info(f"Applying {self.filter_selector.currentText()} filter")
        filter_data = load_filter(
            self.filter_selector.currentText(), spectral_image.get_wavelengths())

        spectral_image.data = spectral_image.data * filter_data

        return spectral_image
