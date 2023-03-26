from PyQt6 import QtWidgets
from src.spectral_to_rgb_modules.band_selector import BandSelector
from src.spectral_to_rgb_modules.observer_conversion_settings import ObserverConversion
from src.conversions.spectral_to_tristimulus import spectral_to_RGB_using_cie_observer, \
    spectral_to_XYZ_using_cie_observer, spectral_to_rgb_using_bands


class SpectralToRGBTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.radio_group = QtWidgets.QGroupBox()

        self.band_selector = BandSelector()
        self.observer_settings = ObserverConversion()

        self.observer_radio = QtWidgets.QRadioButton(
            "Conversion using an Observer", self.radio_group)
        self.observer_radio.toggled.connect(self._update_radio_selection)

        self.band_radio = QtWidgets.QRadioButton("Conversion using three spectral bands",
                                                 self.radio_group)
        self.band_radio.toggled.connect(self._update_radio_selection)
        self.observer_radio.toggle()

        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.band_radio, 0, 0)
        layout.addWidget(self.band_selector, 1, 0)

        layout.addWidget(self.observer_radio, 2, 0)
        layout.addWidget(self.observer_settings, 3, 0)

        layout.setRowStretch(layout.rowCount(), 1)

        self.setLayout(layout)

    def process(self, spectral_image):
        # update values if the min/max wavelength or depth changed
        self.band_selector.update_values(spectral_image)

        if self.band_radio.isChecked():
            image = spectral_to_rgb_using_bands(spectral_image, self.band_selector.get_bands())

        elif self.observer_radio.isChecked():
            step_size = self.observer_settings.get_step_size()
            if self.observer_settings.get_output() == "XYZ":
                image = spectral_to_XYZ_using_cie_observer(spectral_image, step_size)
            elif self.observer_settings.get_output() == "sRGB":
                image = spectral_to_RGB_using_cie_observer(spectral_image, step_size)
            else:
                raise Exception("Unknown observer output")

        return image

    def _update_radio_selection(self, checked):
        # disable the other options
        if checked:
            self.observer_settings.setDisabled(not self.observer_radio.isChecked())
            self.band_selector.setDisabled(not self.band_radio.isChecked())
