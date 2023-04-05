from PyQt6 import QtWidgets, QtGui, QtCore
import logging
from src.data_loader.load_camera import get_camera_names
from src.conversions.spectral_to_tristimulus import spectral_to_RGB_using_camera_response

log = logging.getLogger(__name__)


class CameraConversionModule(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Observer
        observer_label = QtWidgets.QLabel("Camera:")
        self.camera_selector = QtWidgets.QComboBox()
        self.camera_selector.addItems(get_camera_names())

        layout = QtWidgets.QGridLayout()
        layout.addWidget(observer_label, 0, 0)
        layout.addWidget(self.camera_selector, 0, 1)
        layout.setColumnStretch(layout.columnCount(), 1)
        self.setLayout(layout)

    def process(self, spectral_image):
        image = spectral_to_RGB_using_camera_response(
            spectral_image, self.camera_selector.currentText(), 10)
        return image
