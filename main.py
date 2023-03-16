import numpy as np
import sys
from PyQt6 import QtWidgets, QtCore
import cv2
from src.util import load_spectral_image, spectral_to_rgb_from_bands
from src.spectral_viewer import SpectralViewer


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("SpectralViewer")
    viewer = SpectralViewer()
    viewer.show()
    app.exec()


if __name__ == "__main__":
    main()
