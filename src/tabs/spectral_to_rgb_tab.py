from PyQt6 import QtWidgets
from src.spectral_to_rgb_modules.band_conversion_module import BandConversionModule
from src.spectral_to_rgb_modules.observer_conversion_module import ObserverConversionModule
from src.conversions.spectral_to_tristimulus import spectral_to_RGB_using_cie_observer, \
    spectral_to_XYZ_using_cie_observer, spectral_to_rgb_using_bands


class SpectralToRGBTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.radio_group = QtWidgets.QGroupBox()

        self.band_conversion_module = BandConversionModule()
        self.observer_conversion_module = ObserverConversionModule()

        self.observer_radio = QtWidgets.QRadioButton(
            "Conversion using an Observer", self.radio_group)
        self.observer_radio.toggled.connect(self._update_radio_selection)

        self.band_radio = QtWidgets.QRadioButton("Conversion using three spectral bands",
                                                 self.radio_group)
        self.band_radio.toggled.connect(self._update_radio_selection)
        self.observer_radio.toggle()

        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.band_radio, 0, 0)
        layout.addWidget(self.band_conversion_module, 1, 0)
        layout.addWidget(self.observer_radio, 2, 0)
        layout.addWidget(self.observer_conversion_module, 3, 0)
        layout.setRowStretch(layout.rowCount(), 1)

        self.setLayout(layout)

    def process(self, spectral_image):
        if self.band_radio.isChecked():
            return self.band_conversion_module.process(spectral_image)
        elif self.observer_radio.isChecked():
            return self.observer_conversion_module.process(spectral_image)

    def _update_radio_selection(self, checked):
        # disable the other options
        if checked:
            self.observer_conversion_module.setDisabled(not self.observer_radio.isChecked())
            self.band_conversion_module.setDisabled(not self.band_radio.isChecked())
