from PyQt6 import QtWidgets, QtGui
import cv2
import numpy as np
from src.util import load_spectral_image, spectral_to_rgb_from_bands


class SpectralViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout()

        spectral_image, bands = load_spectral_image("./res/images/ARAD_1K_0098.mat")
        rgb = spectral_to_rgb_from_bands(spectral_image)
        rgb = ((rgb / rgb.max()) * 255).astype(np.uint8)
        print(rgb.max())
        h, w, d = rgb.shape
        qimage = QtGui.QImage(rgb.data.tobytes(), w, h, d * w, QtGui.QImage.Format.Format_RGB888)
        print(qimage.format())
        label = QtWidgets.QLabel()
        label.setPixmap(QtGui.QPixmap.fromImage(qimage))

        self.main_layout.addWidget(label)
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

