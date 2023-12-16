import os
import sys
from PyQt6 import QtWidgets
from src.spectral_viewer import SpectralViewer
import logging
import tempfile


def main():
    setup_logger()
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("SpectralViewer")
    viewer = SpectralViewer()
    viewer.show()
    try:
        app.exec()
    except Exception as e:
        print(e)


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    # console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.info(f"Started SpectralViewer")



if __name__ == "__main__":
    main()
