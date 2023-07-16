from PyQt6 import QtWidgets, QtGui, QtCore
import logging
import numpy as np
from src.util.abstract_module import AbstractModule

log = logging.getLogger(__name__)


class ExposureModule(AbstractModule):
    def __init__(self):
        super().__init__()

        self.setToolTip("Change the exposure")

        self.exposure_slider_label = QtWidgets.QLabel("Exposure:")
        self.exposure_slider = QtWidgets.QSlider()
        self.exposure_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.exposure_slider.valueChanged.connect(self._update_exposure_label)
        self.exposure_slider.setMinimum(-40)
        self.exposure_slider.setMaximum(+40)
        self.exposure_slider.setValue(0)
        self.exposure_slider_display = QtWidgets.QLabel(f"±0 stops")

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.exposure_slider_label, 0, 0)
        self.layout.addWidget(self.exposure_slider, 0, 1)
        self.layout.addWidget(self.exposure_slider_display, 0, 2)
        # self.layout.setColumnStretch(2, 2)
        self.layout.addLayout(self.navigation_layout, 0, 3)
        self.setLayout(self.layout)

    def _update_exposure_label(self, value):
        value = value / 4  # allow for more precision
        prefix = ""
        if value > 0:
            prefix = "+"
        elif value == 0:
            prefix = "±"

        postfix = "stops"
        if value == 1 or value == -1:
            postfix = "stop"

        self.exposure_slider_display.setText(f"{prefix}{value:.2f} {postfix}")

    def process(self, image):
        exposure = self.exposure_slider.value()
        return image * 2 ** (exposure / 4)  # /4 to allow for more precision
