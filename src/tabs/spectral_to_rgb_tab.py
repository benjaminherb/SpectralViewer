from PyQt6 import QtWidgets
from src.spectral_to_rgb_modules.band_conversion_module import BandConversionModule
from src.spectral_to_rgb_modules.observer_conversion_module import ObserverConversionModule
from src.spectral_to_rgb_modules.camera_conversion_module import CameraConversionModule


class SpectralToRGBTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.radio_group = QtWidgets.QGroupBox()

        self.band_conversion_module = BandConversionModule()
        self.band_radio = QtWidgets.QRadioButton(
            "Conversion using three spectral bands", self.radio_group)
        self.band_radio.toggled.connect(self._update_radio_selection)

        self.observer_conversion_module = ObserverConversionModule()
        self.observer_radio = QtWidgets.QRadioButton(
            "Conversion using an observer", self.radio_group)
        self.observer_radio.toggled.connect(self._update_radio_selection)

        self.camera_conversion_module = CameraConversionModule()
        self.camera_radio = QtWidgets.QRadioButton(
            "Conversion using a camera response", self.radio_group)
        self.camera_radio.toggled.connect(self._update_radio_selection)

        self.observer_radio.toggle()  # default

        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.band_radio, 0, 0)
        layout.addWidget(self.band_conversion_module, 1, 0)
        layout.addWidget(self.observer_radio, 2, 0)
        layout.addWidget(self.observer_conversion_module, 3, 0)
        layout.addWidget(self.camera_radio, 4, 0)
        layout.addWidget(self.camera_conversion_module, 5, 0)
        layout.setRowStretch(layout.rowCount(), 1)

        self.setLayout(layout)

    def process(self, spectral_image):
        if self.band_radio.isChecked():
            return self.band_conversion_module.process(spectral_image)
        elif self.observer_radio.isChecked():
            return self.observer_conversion_module.process(spectral_image)
        elif self.camera_radio.isChecked():
            return self.camera_conversion_module.process(spectral_image)

    def _update_radio_selection(self, checked):
        # disable the other options
        if checked:
            self.band_conversion_module.setDisabled(not self.band_radio.isChecked())
            self.observer_conversion_module.setDisabled(not self.observer_radio.isChecked())
            self.camera_conversion_module.setDisabled(not self.camera_radio.isChecked())
