from PyQt6 import QtWidgets, QtCore, QtGui
from datetime import datetime
import numpy as np
import colour


class AnalyzeTab(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.operations = []

        self.snapshot_01 = None
        self.snapshot_label_01 = QtWidgets.QLabel("Snapshot 1:")
        self.snapshot_text_01 = QtWidgets.QLineEdit("Empty")
        self.snapshot_text_01.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.snapshot_text_01.setDisabled(True)
        self.snapshot_text_01.setMinimumWidth(120)
        self.snapshot_save_button_01 = QtWidgets.QPushButton("Save snapshot")
        self.snapshot_save_button_01.clicked.connect(lambda: self._save(1))
        self.snapshot_show_button_01 = QtWidgets.QPushButton("Show snapshot")
        self.snapshot_show_button_01.clicked.connect(lambda: self._show("S1"))

        self.snapshot_02 = None
        self.snapshot_label_02 = QtWidgets.QLabel("Snapshot 2:")
        self.snapshot_text_02 = QtWidgets.QLineEdit("Empty")
        self.snapshot_text_02.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.snapshot_text_02.setDisabled(True)
        self.snapshot_text_02.setMinimumWidth(120)
        self.snapshot_save_button_02 = QtWidgets.QPushButton("Save snapshot")
        self.snapshot_save_button_02.clicked.connect(lambda: self._save(2))
        self.snapshot_show_button_02 = QtWidgets.QPushButton("Show snapshot")
        self.snapshot_show_button_02.clicked.connect(lambda: self._show("S2"))

        self.difference = None
        self.difference_label = QtWidgets.QLabel("Difference:")
        self.difference_text = QtWidgets.QLineEdit("Empty")
        self.difference_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.difference_text.setDisabled(True)
        self.difference_text.setMinimumWidth(120)
        self.difference_show_button = QtWidgets.QPushButton("Show difference")
        self.difference_show_button.clicked.connect(lambda: self._show("Diff"))

        self.layout = QtWidgets.QGridLayout()  # main layout
        self.layout.addWidget(self.snapshot_label_01, 0, 0)
        self.layout.addWidget(self.snapshot_text_01, 0, 1)
        self.layout.addWidget(self.snapshot_save_button_01, 0, 2)
        self.layout.addWidget(self.snapshot_show_button_01, 0, 3)
        self.layout.addWidget(self.snapshot_label_02, 1, 0)
        self.layout.addWidget(self.snapshot_text_02, 1, 1)
        self.layout.addWidget(self.snapshot_save_button_02, 1, 2)
        self.layout.addWidget(self.snapshot_show_button_02, 1, 3)
        self.layout.addWidget(self.difference_label, 2, 0)
        self.layout.addWidget(self.difference_text, 2, 1)
        self.layout.addWidget(self.difference_show_button, 2, 3)
        self.layout.setColumnStretch(4, 1)
        self.layout.setRowStretch(3, 1)
        self.setLayout(self.layout)

    def _save(self, slot):
        image = self.parent.load_image()
        if slot == 1:
            self.snapshot_01 = image
            self.snapshot_text_01.setText(datetime.now().strftime("%H:%M:%S"))
        if slot == 2:
            self.snapshot_02 = image
            self.snapshot_text_02.setText(datetime.now().strftime("%H:%M:%S"))

    def _show(self, image):
        if image == "S1":
            self.parent.display_image(self.snapshot_01)
        if image == "S2":
            self.parent.display_image(self.snapshot_02)
        if image == "Diff":
            if self.snapshot_01 is not None and self.snapshot_02 is not None:
                self._calculate_difference()
                self.parent.display_image(self.difference)

    def _calculate_difference(self):
        if self.snapshot_01 is not None and self.snapshot_02 is not None:
            self.difference = np.absolute(self.snapshot_01 - self.snapshot_02)
            self.difference_text.setText(f"{np.mean(self.difference):.8f}")
