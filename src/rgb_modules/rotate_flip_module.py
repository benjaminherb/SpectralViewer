import numpy as np
from src.util.abstract_module import AbstractModule
from PyQt6 import QtWidgets


class RotateFlipModule(AbstractModule):
    def __init__(self):
        super().__init__()

        self.setToolTip("Change illuminant")
        self.rotate_label = QtWidgets.QLabel("Rotate")
        self.rotate_selector = QtWidgets.QComboBox()
        self.rotate_selector.addItems(["0", "90", "180", "270"])
        self.vertical_flip_selector = QtWidgets.QCheckBox("Flip vertically")
        self.vertical_flip_selector.setChecked(False)
        self.horizontal_flip_selector = QtWidgets.QCheckBox("Flip horizontally")
        self.horizontal_flip_selector.setChecked(False)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.rotate_label)
        self.layout.addWidget(self.rotate_selector)
        self.layout.addWidget(self.horizontal_flip_selector)
        self.layout.addWidget(self.vertical_flip_selector)
        self.layout.addStretch()
        self.layout.addLayout(self.navigation_layout)
        self.setLayout(self.layout)

    def process(self, image):
        # the index indicates how often the image is rotated by 90°
        image = np.rot90(image, self.rotate_selector.currentIndex(), (0, 1))

        if self.vertical_flip_selector.isChecked():
            image = np.flipud(image)
        if self.horizontal_flip_selector.isChecked():
            image = np.fliplr(image)
        return image
