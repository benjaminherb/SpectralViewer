from PyQt6 import QtWidgets, QtGui, QtCore
import numpy as np
import logging
from src.data_loader.load_camera import get_camera_names
from src.data_loader.load_illuminants import get_illuminant_names
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

        self.reflectance_label = QtWidgets.QLabel("Reflectance Set:")
        self.reflectance_set_selector = QtWidgets.QComboBox()
        self.reflectance_set_selector.addItems(['Macbeth ColorChecker Classic'])

        self.camera_illuminant_label = QtWidgets.QLabel("Camera Illuminant:")
        self.camera_illuminant_selector = QtWidgets.QComboBox()
        self.camera_illuminant_selector.addItems(get_illuminant_names())
        self.reference_illuminant_label = QtWidgets.QLabel("Reference Illuminant:")
        self.reference_illuminant_selector = QtWidgets.QComboBox()
        self.reference_illuminant_selector.addItems(get_illuminant_names())

        layout = QtWidgets.QGridLayout()
        layout.addWidget(observer_label, 0, 0)
        layout.addWidget(self.camera_selector, 0, 1)
        layout.addWidget(self.characterisation_label, 1, 0)
        layout.addWidget(self.characterisation_checkbox, 1, 1)
        layout.addWidget(self.reflectance_label, 2, 0)
        layout.addWidget(self.reflectance_set_selector, 2, 1)
        layout.addWidget(self.camera_illuminant_label, 3, 0)
        layout.addWidget(self.camera_illuminant_selector, 3, 1)
        layout.addWidget(self.reference_illuminant_label, 4, 0)
        layout.addWidget(self.reference_illuminant_selector, 4, 1)
        layout.setAlignment(self.characterisation_checkbox, QtCore.Qt.AlignmentFlag.AlignHCenter)
        layout.setColumnStretch(layout.columnCount(), 1)
        self.setLayout(layout)

    def process(self, spectral_image):
        image = spectral_to_RGB_using_camera_response(
            spectral_image, self.camera_selector.currentText(), 10)
        if self.characterisation_checkbox.isChecked():
            matrix = get_camera_characterisation_matrix(
                self.camera_selector.currentText(),
                self.reflectance_set_selector.currentText(),
                self.camera_illuminant_selector.currentText(),
                self.reference_illuminant_selector.currentText()
                )
            image = np.dot(image, matrix)
        return image
