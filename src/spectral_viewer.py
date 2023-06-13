from PyQt6 import QtWidgets, QtGui, QtCore
import numpy as np
from copy import deepcopy
import logging
from src.tabs.source_tab import SourceTab
from src.tabs.spectral_to_rgb_tab import SpectralToRGBTab
from src.tabs.picker_tab import PickerTab
from src.tabs.rgb_operations_tab import RGBOperationsTab
from src.tabs.spectral_operations_tab import SpectralOperationsTab
from src.tabs.spectrogram_tab import SpectrogramTab
from src.tabs.analyze_tab import AnalyzeTab
from src.gui.preview_image import PreviewImage

log = logging.getLogger(__name__)


class SpectralViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SpectralViewer")

        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # control panel
        self.control_widget = QtWidgets.QWidget()
        self.control_widget.setMinimumWidth(900)

        # tabs
        self.source_tab = SourceTab()
        self.picker_tab = PickerTab()
        self.spectrogram_tab = SpectrogramTab()
        self.spectral_operations_tab = SpectralOperationsTab()
        self.spectral_to_rgb_tab = SpectralToRGBTab()
        self.rgb_operations_tab = RGBOperationsTab()
        self.analyze_tab = AnalyzeTab(self)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.tabBarClicked.connect(self.tab_bar_was_clicked)
        self.tabs.addTab(self.source_tab, "Source")
        self.tabs.addTab(self.picker_tab, "Pixel Picker")
        self.tabs.addTab(self.spectrogram_tab, "Spectrogram")
        self.tabs.addTab(self.spectral_operations_tab, "Spectral Operations")
        self.tabs.addTab(self.spectral_to_rgb_tab, "Spectral to RGB")
        self.tabs.addTab(self.rgb_operations_tab, "RGB Operations")
        self.tabs.addTab(self.analyze_tab, "Analyze")

        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self.refresh_button.pressed.connect(self.show_preview_image)

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
        self.show_preview_image()

        # Add hotkey for refresh
        self.hotkey = QtGui.QShortcut(QtCore.Qt.Key.Key_R, self)
        self.hotkey.activated.connect(self.show_preview_image)

    def process_image(self):
        log.info("Loading image")
        spectral_image = self.source_tab.get_image()

        # image processing
        spectral_image = self.spectral_operations_tab.process(spectral_image)
        image = self.spectral_to_rgb_tab.process(spectral_image)
        image = self.rgb_operations_tab.process(image)

        return image

    def display_image(self, image):
        # display image
        h, w, d = image.shape
        image = (image * 255).astype(np.uint8)
        q_image = QtGui.QImage(image.data.tobytes(), w, h, d * w,
                               QtGui.QImage.Format.Format_RGB888)
        self.image.setPixmap(QtGui.QPixmap.fromImage(q_image))

    def show_preview_image(self):
        image = self.process_image()
        self.display_image(image)

    def tab_bar_was_clicked(self, index):
        if self.tabs.widget(index) == self.picker_tab:
            spectral_image = self.source_tab.get_image()
            processed_spectral_image = self.spectral_operations_tab.process(
                deepcopy(spectral_image))
            self.picker_tab.update_plot(spectral_image, processed_spectral_image)

        if self.tabs.widget(index) == self.spectrogram_tab:
            spectral_image = self.source_tab.get_image()
            processed_spectral_image = self.spectral_operations_tab.process(
                deepcopy(spectral_image))
            self.spectrogram_tab.plot(spectral_image, processed_spectral_image)

    def mouse_move_over_image(self, x, y):
        if self.picker_tab.isVisible():
            # pixel_position = self.image.mapFromParent(event.pos())
            self.picker_tab.show_position((x, y))

    def mouse_clicked_on_image(self, x, y):
        if self.picker_tab.isVisible():
            spectral_image = self.source_tab.get_image()
            processed_spectral_image = self.spectral_operations_tab.get_processed_spectral_image()
            rgb_image = self.rgb_operations_tab.get_processed_image()
            self.picker_tab.plot((x, y), spectral_image, processed_spectral_image, rgb_image)

        if self.source_tab.white_reference_button.isChecked():
            self.source_tab.set_white_reference(x, y)
