from PyQt6 import QtWidgets
from src.gui.band_selector import BandSelector


class SpectralToRGBTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.band_selector = BandSelector()
        layout.addWidget(self.band_selector)
        self.setLayout(layout)

    def get_bands(self):
        return self.band_selector.get_bands()