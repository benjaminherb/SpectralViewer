from PyQt6 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import numpy as np


class SpectrogramTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.pre_pen = pg.mkPen('#0000AA', width=1)
        self.post_pen = pg.mkPen('#AA0000', width=1)
        pg.setConfigOption('foreground', 'k')
        # evil bad workaround as the color is not defined in its palette
        pg.setConfigOption('background', (251, 251, 251, 255))

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.addLegend()
        self.plot_widget.plotItem.setMouseEnabled(x=False)  # Only allow zoom in Y-axis
        self.plot_widget.setYRange(0, 1)
        self.plot_widget.plotItem.getViewBox().setLimits(yMin=0, yMax=1)  # limit zoom range

        self.plot_widget.plotItem.setMenuEnabled(False)
        self.plot_widget.plotItem.setLabel(axis='left', text='Average Intensity [0,1]')
        self.plot_widget.plotItem.setLabel(axis='bottom', text='Wavelength', units="nm")

        self.plot_widget.plot(np.arange(0, 31) * 10 + 400, np.zeros(31)) # default range 400-700
        self.plot_widget.setBackground("default")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def plot(self, spectral_image, processed_spectral_image):
        self.plot_widget.getPlotItem().clear()
        value_count = spectral_image.width() * spectral_image.height()
        spectrogram = spectral_image.data.sum(axis=(0, 1)) / value_count
        processed_spectrogram = processed_spectral_image.data.sum(axis=(0, 1)) / value_count
        self.plot_widget.plot(spectral_image.get_wavelengths(),
                              spectrogram, pen=self.pre_pen, name="Original")
        self.plot_widget.plot(processed_spectral_image.get_wavelengths(),
                              processed_spectrogram, pen=self.post_pen, name="Processed")
