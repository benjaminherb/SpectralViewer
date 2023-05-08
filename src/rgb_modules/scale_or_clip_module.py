from PyQt6 import QtWidgets, QtGui
import logging
import numpy as np
from src.util.abstract_module import AbstractModule

log = logging.getLogger(__name__)


class ScaleOrClipModule(AbstractModule):
    def __init__(self):
        super().__init__()

        self.setToolTip("Scale or clip pixel values")

        self.minimum_label = QtWidgets.QLabel("Minimum Values:")
        self.minimum_selector = QtWidgets.QComboBox()
        self.minimum_selector.addItems(['None', 'Clip', 'Offset'])
        self.minimum_selector.setCurrentText('Clip')
        self.maximum_label = QtWidgets.QLabel("Maximum Values:")
        self.maximum_selector = QtWidgets.QComboBox()
        self.maximum_selector.addItems(['None', 'Clip', 'Scale to 1'])
        self.maximum_selector.setCurrentText('Scale to 1')

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.minimum_label, 0, 0)
        self.layout.addWidget(self.minimum_selector, 0, 1)
        self.layout.addWidget(self.maximum_label, 1, 0)
        self.layout.addWidget(self.maximum_selector, 1, 1)
        self.layout.setColumnStretch(2, 2)
        self.layout.addLayout(self.navigation_layout, 0,3)
        self.setLayout(self.layout)

    def process(self, image):
        if self.minimum_selector.currentText() == 'Offset':
            image = image - image.min()
        elif self.minimum_selector.currentText() == "Clip":
            image = np.clip(image, a_min=0, a_max=None)

        if self.maximum_selector.currentText() == 'Scale to 1':
            image = image / image.max()
        elif self.maximum_selector.currentText() == "Clip":
            image = np.clip(image, a_min=None, a_max=1)

        return image
