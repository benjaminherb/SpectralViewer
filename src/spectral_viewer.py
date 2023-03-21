from PyQt6 import QtWidgets, QtGui, QtCore
import numpy as np
from src.gui.source_tab import SourceTab
from src.gui.spectral_to_rgb_tab import SpectralToRGBTab
from src.conversions.tristimulus import linear_to_sRGB
import pyqtgraph


class SpectralViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QHBoxLayout()

        # control panel
        self.control_widget = QtWidgets.QWidget()
        self.control_widget.setMinimumWidth(800)

        # tabs
        self.source_tab = SourceTab()
        self.spectral_to_rgb_tab = SpectralToRGBTab()

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.source_tab, "Source")
        self.tabs.addTab(QtWidgets.QWidget(), "Spectral Operations")
        self.tabs.addTab(self.spectral_to_rgb_tab, "Spectral to RGB")
        self.tabs.addTab(QtWidgets.QWidget(), "RGB Operations")
        self.tabs.addTab(QtWidgets.QWidget(), "Export")

        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self.refresh_button.pressed.connect(self.load_image)

        self.control_layout = QtWidgets.QGridLayout()
        self.control_layout.addWidget(self.tabs)
        self.control_layout.addWidget(self.refresh_button)
        self.control_widget.setLayout(self.control_layout)

        pyqtgraph.setConfigOption('foreground', 'k')
        image_layout = QtWidgets.QVBoxLayout()
        image_widget = QtWidgets.QWidget()
        self.image = QtWidgets.QLabel()
        self.image.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                 QtWidgets.QSizePolicy.Policy.Minimum)
        self.spectral_picker_plot = pyqtgraph.PlotWidget()
        self.spectral_picker_plot.plot(np.arange(0, 31) * 10 + 400, np.zeros(31))
        self.spectral_picker_plot.setBackground(
            QtWidgets.QMainWindow().palette().color(QtGui.QPalette.ColorRole.Window))

        image_layout.addWidget(self.image)
        image_layout.addWidget(self.spectral_picker_plot)
        image_widget.setLayout(image_layout)

        self.main_layout.addWidget(image_widget)
        self.main_layout.addWidget(self.control_widget)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.load_image()

    def load_image(self):
        self.source_tab.load_image()
        spectral_image = self.source_tab.spectral_image
        rgb = self.spectral_to_rgb_tab.process(spectral_image)
        rgb = rgb.clip(min=0)
        rgb = linear_to_sRGB(rgb)
        rgb = ((rgb / rgb.max()) * 255).astype(np.uint8)
        rgb = np.clip(rgb, a_max=255, a_min=0)
        h, w, d = rgb.shape
        q_image = QtGui.QImage(rgb.data.tobytes(), w, h, d * w, QtGui.QImage.Format.Format_RGB888)

        self.image.setPixmap(QtGui.QPixmap.fromImage(q_image))

    def mousePressEvent(self, event):
        pixel_position = self.image.mapFromGlobal(event.pos())
        spectral_image = self.source_tab.spectral_image
        width, height, _ = spectral_image.shape
        if pixel_position.x() in range(0, width) and pixel_position.y() in range(0, height):
            self.spectral_picker_plot.getPlotItem().clear()
            spectral_pixel_values = spectral_image[pixel_position.y(), pixel_position.x()]
            self.spectral_picker_plot.plot(
                np.arange(0, 31) * 10 + 400, spectral_pixel_values,
                pen=pyqtgraph.mkPen('k', width=2))

        super().mousePressEvent(event)
