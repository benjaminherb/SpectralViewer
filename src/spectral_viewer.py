from PyQt6 import QtWidgets, QtGui
import cv2
import numpy as np
from src.util import load_spectral_image, spectral_to_rgb_from_bands
from src.gui.control_widget import ControlWidget


class SpectralViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.control_widget = ControlWidget()
        self.control_widget.update_signal.connect(self.load_image)

        self.image = QtWidgets.QLabel()
        self.main_layout.addWidget(self.image)
        self.main_layout.addWidget(self.control_widget)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.load_image()

    def load_image(self):
        spectral_image, bands = load_spectral_image("./res/images/ARAD_1K_0098.mat")
        rgb = spectral_to_rgb_from_bands(spectral_image, self.control_widget.get_bands())
        rgb = ((rgb / rgb.max()) * 255).astype(np.uint8)
        h, w, d = rgb.shape
        q_image = QtGui.QImage(rgb.data.tobytes(), w, h, d * w, QtGui.QImage.Format.Format_RGB888)
        self.image.setPixmap(QtGui.QPixmap.fromImage(q_image))
