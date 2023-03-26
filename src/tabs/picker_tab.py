from PyQt6 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import numpy as np


class PickerTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.graph_pen = pg.mkPen('k', width=1)

        pg.setConfigOption('foreground', 'k')
        # evil bad workaround as the color is not defined in its palette
        pg.setConfigOption('background', (251, 251, 251, 255))

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.plotItem.setMouseEnabled(x=False)  # Only allow zoom in Y-axis
        self.plot_widget.setYRange(0, 1)
        self.plot_widget.plotItem.getViewBox().setLimits(yMin=0, yMax=1)  # limit zoom range

        self.plot_widget.plotItem.setMenuEnabled(False)
        self.plot_widget.plotItem.setLabel(axis='left', text='Intensity [0,1]')
        self.plot_widget.plotItem.setLabel(axis='bottom', text='Wavelength [nm]')

        # self.plot_widget.setYRange(0, 1)
        self.plot_widget.plot(np.arange(0, 31) * 10 + 400, np.zeros(31))
        self.plot_widget.setBackground("default")

        self.position_label = QtWidgets.QLabel()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.position_label)
        self.setLayout(layout)

    def plot(self, pixel_position, spectral_image):
        x, y = pixel_position
        height, width, _ = spectral_image.shape
        if x in range(0, width) and y in range(0, height):
            self.plot_widget.getPlotItem().clear()
            spectral_pixel_values = spectral_image[y, x]
            self.plot_widget.plot(
                np.arange(0, 31) * 10 + 400, spectral_pixel_values,
                pen=self.graph_pen)
            self.plot_widget.setYRange(0, 1)

    def show_position(self, position):
        x, y = position
        self.position_label.setText(f"Position: {x},{y}")