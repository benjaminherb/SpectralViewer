from PyQt6 import QtWidgets, QtGui, QtCore
import numpy as np
from src.gui.source_tab import SourceTab
from src.gui.spectral_to_rgb_tab import SpectralToRGBTab
from src.gui.picker_tab import PickerTab
from src.gui.rgb_operations_tab import RGBOperationsTab
from src.gui.spectral_operations_tab import SpectralOperationsTab
from src.gui.preview_image import PreviewImage


class SpectralViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SpectralViewer")

        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # control panel
        self.control_widget = QtWidgets.QWidget()
        self.control_widget.setMinimumWidth(800)

        # tabs
        self.source_tab = SourceTab()
        self.spectral_operations_tab = SpectralOperationsTab()
        self.spectral_to_rgb_tab = SpectralToRGBTab()
        self.rgb_operations_tab = RGBOperationsTab()
        self.picker_tab = PickerTab()

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.source_tab, "Source")
        self.tabs.addTab(self.picker_tab, "Pixel Picker")
        self.tabs.addTab(self.spectral_operations_tab, "Spectral Operations")
        self.tabs.addTab(self.spectral_to_rgb_tab, "Spectral to RGB")
        self.tabs.addTab(self.rgb_operations_tab, "RGB Operations")
        self.tabs.addTab(QtWidgets.QWidget(), "Export")

        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self.refresh_button.pressed.connect(self.load_image)

        self.control_layout = QtWidgets.QGridLayout()
        self.control_layout.addWidget(self.tabs)
        self.control_layout.addWidget(self.refresh_button)
        self.control_widget.setLayout(self.control_layout)

        self.image = PreviewImage()
        self.image.mouse_moved.connect(self.mouse_move_over_image)
        self.image.mouse_clicked.connect(self.mouse_clicked_on_image)

        self.main_layout.addWidget(self.image)
        self.main_layout.addWidget(self.control_widget)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.load_image()

    def load_image(self):
        self.source_tab.load_image()
        spectral_image = self.source_tab.spectral_image
        rgb = self.spectral_to_rgb_tab.process(spectral_image)
        rgb = rgb.clip(min=0)
        rgb = self.rgb_operations_tab.process(rgb)
        # rgb = linear_to_sRGB(rgb)
        rgb = ((rgb / rgb.max()) * 255).astype(np.uint8)
        rgb = np.clip(rgb, a_max=255, a_min=0)
        h, w, d = rgb.shape
        q_image = QtGui.QImage(rgb.data.tobytes(), w, h, d * w, QtGui.QImage.Format.Format_RGB888)

        self.image.setPixmap(QtGui.QPixmap.fromImage(q_image))

    def mouse_move_over_image(self, x, y):
        if self.picker_tab.isVisible():
            # pixel_position = self.image.mapFromParent(event.pos())
            self.picker_tab.show_position((x, y))

    def mouse_clicked_on_image(self, x, y):
        if self.picker_tab.isVisible():
            spectral_image = self.source_tab.spectral_image
            self.picker_tab.plot((x, y), spectral_image)
