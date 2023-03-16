import sys
from PyQt6 import QtWidgets
from src.spectral_viewer import SpectralViewer


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("SpectralViewer")
    viewer = SpectralViewer()
    viewer.show()
    app.exec()


if __name__ == "__main__":
    main()
