from PyQt6 import QtWidgets


# from src import MIN_WAVELENGTH, MAX_WAVELENGTH, BAND_COUNT


class BandSelector(QtWidgets.QWidget):
    def __init__(self, minimum_wavelength=400, maximum_wavelength=700, bandcount=31):
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.minimum_wavelength = minimum_wavelength
        self.maximum_wavelength = maximum_wavelength
        self.bandcount = bandcount

        self.band0_label = QtWidgets.QLabel("Red (nm):")
        self.band0 = self._get_single_selector(.8)
        self.band1_label = QtWidgets.QLabel("Green (nm):")
        self.band1 = self._get_single_selector(.5)
        self.band2_label = QtWidgets.QLabel("Blue (nm):")
        self.band2 = self._get_single_selector(.2)

        self.layout.addWidget(self.band0_label)
        self.layout.addWidget(self.band0)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.band1_label)
        self.layout.addWidget(self.band1)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.band2_label)
        self.layout.addWidget(self.band2)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def get_bands(self):
        step = self.get_step()
        return int((self.band0.value() - self.minimum_wavelength) / step), \
            int((self.band1.value() - self.minimum_wavelength) / step), \
            int((self.band2.value() - self.minimum_wavelength) / step)

    def _get_single_selector(self, percentage):
        step = self.get_step()
        band = QtWidgets.QSpinBox()
        band.setMinimum(self.minimum_wavelength)
        band.setMaximum(self.maximum_wavelength)
        band.setSingleStep(step)
        band.setValue(int(percentage * self.bandcount) * step + self.minimum_wavelength)
        return band

    def get_step(self):
        return int((self.maximum_wavelength - self.minimum_wavelength) / (self.bandcount - 1))

    def update_values(self, spectral_image):
        # updated internal variables and reset to default if something changed
        if (self.minimum_wavelength != spectral_image.minimum_wavelength or
                self.maximum_wavelength != spectral_image.maximum_wavelength or
                self.bandcount != spectral_image.depth()):

            self.minimum_wavelength = spectral_image.minimum_wavelength
            self.maximum_wavelength = spectral_image.maximum_wavelength
            self.bandcount = spectral_image.depth()

            step = self.get_step()
            for band, percentage in zip([self.band0, self.band1, self.band2], [0.8, 0.5, 0.2]):
                band.setMinimum(self.minimum_wavelength)
                band.setMaximum(self.maximum_wavelength)
                band.setSingleStep(step)
                band.setValue(int(percentage * self.bandcount) * step + self.minimum_wavelength)
