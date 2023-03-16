from PyQt6 import QtWidgets, QtCore
from src.gui.spectral_to_rgb.spectral_to_rgb_tab import SpectralToRGBTab


class ControlWidget(QtWidgets.QWidget):
    update_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QGridLayout()
        self.setMinimumWidth(800)

        self.tabs = QtWidgets.QTabWidget()

        self.spectral_to_rgb_tab = SpectralToRGBTab()

        self.tabs.addTab(QtWidgets.QWidget(), "Load Image")
        self.tabs.addTab(QtWidgets.QWidget(), "Spectral Operations")
        self.tabs.addTab(self.spectral_to_rgb_tab, "Spectral to RGB")
        self.tabs.addTab(QtWidgets.QWidget(), "RGB Operations")
        self.tabs.addTab(QtWidgets.QWidget(), "Export")

        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self.refresh_button.pressed.connect(self.update_signal)

        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)

    def get_bands(self):
        return self.spectral_to_rgb_tab.band_selector.get_bands()
