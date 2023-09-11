from PyQt6 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import numpy as np

from src.gui.formatted_yaxis_item import FormattedYAxisItem


class PickerTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.previous_pixel_position = (-1, -1)  # used for updating data without new position

        self.pre_pen = pg.mkPen('#0000AA', width=3)
        self.post_pen = pg.mkPen('#AA0000', width=3)
        # pg.setConfigOption('foreground', 'w')
        # evil bad workaround as the color is not defined in its palette
        pg.setConfigOption('background', (0, 0, 0, 0))
        pg.setConfigOption('foreground', (0, 0, 0, 255))

        self.plot_widget = pg.PlotWidget(axisItems={'left': FormattedYAxisItem(orientation='left')})
        self.plot_widget.addLegend()

        # let the plot blend in with the background
        # self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.plot_widget.setStyleSheet("background-color:transparent;")

        self.plot_widget.plotItem.setMouseEnabled(x=False)  # Only allow zoom in Y-axis
        self.plot_widget.setYRange(0, 1)
        self.plot_widget.plotItem.getViewBox().setLimits(yMin=0, yMax=1, minYRange=0.04)  # limit zoom range

        self.plot_widget.plotItem.setMenuEnabled(False)
        self.plot_widget.plotItem.setLabel(axis='left', text='relative radiance [0,1]')
        self.plot_widget.plotItem.setLabel(axis='bottom', text='wavelength [nm]')
        self.plot_widget.plot(np.arange(0, 31) * 10 + 400, np.zeros(31))
        self.plot_widget.setBackground("default")

        self.position_label = QtWidgets.QLabel()
        self.picked_data_label = QtWidgets.QLabel()
        self.plot_choice_selector = QtWidgets.QComboBox()
        self.plot_choice_selector.addItems(['original & processed', 'original', 'processed'])
        self.plot_choice_selector.currentIndexChanged.connect(parent.update_spectral_plots)
        self.plot_values_selector = QtWidgets.QComboBox()
        self.plot_values_selector.addItems(['plot position', 'plot mean'])
        self.plot_values_selector.currentIndexChanged.connect(parent.update_spectral_plots)

        info_layout = QtWidgets.QHBoxLayout()
        info_layout.addWidget(self.position_label)
        info_layout.addWidget(self.picked_data_label)
        info_layout.addSpacing(10)
        info_layout.addWidget(self.plot_values_selector)
        info_layout.addWidget(self.plot_choice_selector)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(info_layout)
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def plot(self, pixel_position, spectral_image, processed_spectral_image, rgb_image=None):
        x, y = pixel_position
        if x in range(0, spectral_image.width()) and y in range(0, spectral_image.height()):
            self.plot_widget.getPlotItem().clear()

            if self.plot_values_selector.currentText() == 'plot mean':
                spectral_pixel_values = np.mean(spectral_image.data, axis=(0, 1))
                processed_spectral_pixel_values = np.mean(processed_spectral_image.data, axis=(0, 1))
            else:
                spectral_pixel_values = spectral_image.data[y, x]
                processed_spectral_pixel_values = processed_spectral_image.data[y, x]

            if self.plot_choice_selector.currentText() in ('original', 'original & processed'):
                self.plot_widget.plot(spectral_image.get_wavelengths(),
                                      spectral_pixel_values,
                                      pen=self.pre_pen, name="Original")

            if self.plot_choice_selector.currentText() in ('processed', 'original & processed'):
                self.plot_widget.plot(processed_spectral_image.get_wavelengths(),
                                      processed_spectral_pixel_values,
                                      pen=self.post_pen, name=f"Processed")

            if rgb_image is not None:
                self.picked_data_label.setText(
                    f" RGB: {rgb_image[x, y][0]:.3f} / {rgb_image[x, y][1]:.3f} / {rgb_image[x, y][2]:.3f}")

            self.previous_pixel_position = pixel_position

    def update_plot(self, spectral_image, processed_spectral_image):
        self.plot(self.previous_pixel_position, spectral_image, processed_spectral_image)

    def show_position(self, position):
        x, y = position
        self.position_label.setText(
            f"Position: {self.previous_pixel_position[0]}, {self.previous_pixel_position[1]} ({x},{y})")