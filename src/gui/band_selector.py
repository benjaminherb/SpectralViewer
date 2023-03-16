from PyQt6 import QtWidgets
from src import MIN_WAVELENGTH, MAX_WAVELENGTH, BAND_COUNT


class BandSelector(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout()

        self.band0_label = QtWidgets.QLabel("Red (nm):")
        self.band0 = _get_single_selector(.8)
        self.band1_label = QtWidgets.QLabel("Green (nm):")
        self.band1 = _get_single_selector(.5)
        self.band2_label = QtWidgets.QLabel("Blue (nm):")
        self.band2 = _get_single_selector(.2)

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
        step = get_step()
        return int((self.band0.value() - MIN_WAVELENGTH) / step), \
            int((self.band1.value() - MIN_WAVELENGTH) / step), \
            int((self.band2.value() - MIN_WAVELENGTH) / step)


def _get_single_selector(percentage):
    step = get_step()
    band = QtWidgets.QSpinBox()
    band.setMinimum(MIN_WAVELENGTH)
    band.setMaximum(MAX_WAVELENGTH)
    band.setSingleStep(step)
    band.setValue(int(percentage * BAND_COUNT) * step + MIN_WAVELENGTH)
    return band


def get_step():
    return int((MAX_WAVELENGTH - MIN_WAVELENGTH) / (BAND_COUNT - 1))
