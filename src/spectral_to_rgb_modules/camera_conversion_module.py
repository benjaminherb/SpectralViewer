from PyQt6 import QtWidgets, QtGui, QtCore
import numpy as np
import logging
from src.data_loader.load_camera import get_camera_names
from src.conversions.spectral_to_tristimulus import spectral_to_RGB_using_camera_response
from src.conversions.matrices import get_camera_characterisation_matrix

log = logging.getLogger(__name__)


class CameraConversionModule(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Observer
        observer_label = QtWidgets.QLabel("Camera Response:")
        self.camera_selector = QtWidgets.QComboBox()
        self.camera_selector.addItems(get_camera_names())
        self.characterisation_label = QtWidgets.QLabel("Characterization Matrix:")
        self.characterisation_checkbox = QtWidgets.QCheckBox("Apply")

        layout = QtWidgets.QGridLayout()
        layout.addWidget(observer_label, 0, 0)
        layout.addWidget(self.camera_selector, 0, 1)
        layout.addWidget(self.characterisation_label, 1, 0)
        layout.addWidget(self.characterisation_checkbox, 1, 1)
        layout.setAlignment(self.characterisation_checkbox, QtCore.Qt.AlignmentFlag.AlignHCenter)
        layout.setColumnStretch(layout.columnCount(), 1)
        self.setLayout(layout)

    def process(self, spectral_image):
        image = spectral_to_RGB_using_camera_response(
            spectral_image, self.camera_selector.currentText(), 10)
        if self.characterisation_checkbox.isChecked():
            matrix = get_camera_characterisation_matrix(self.camera_selector.currentText())
            image = np.dot(image, matrix)
        return image
