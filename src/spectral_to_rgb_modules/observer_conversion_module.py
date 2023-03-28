from PyQt6 import QtWidgets, QtGui, QtCore
from src.conversions.spectral_to_tristimulus import spectral_to_RGB_using_cie_observer, \
    spectral_to_XYZ_using_cie_observer


class ObserverConversionModule(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Observer
        observer_label = QtWidgets.QLabel("Observer:")
        self.observer_selector = QtWidgets.QComboBox()
        self.observer_selector.addItems(["CIE 1931"])
        observer_label_2 = QtWidgets.QLabel("in")
        self.observer_step_size_selector = QtWidgets.QComboBox()
        self.observer_step_size_selector.addItems(["1", "2", "5", "10"])
        self.observer_step_size_selector.setCurrentText("10")
        observer_label_3 = QtWidgets.QLabel("nm steps")

        # Output
        output_label = QtWidgets.QLabel("Output:")
        self.output_selector = QtWidgets.QComboBox()
        self.output_selector.addItems(["sRGB", "XYZ"])

        layout = QtWidgets.QGridLayout()
        layout.addWidget(observer_label, 0, 0)
        layout.addWidget(self.observer_selector, 0, 1)
        layout.addWidget(observer_label_2, 0, 2)
        layout.addWidget(self.observer_step_size_selector, 0, 3)
        layout.addWidget(observer_label_3, 0, 4)
        layout.addWidget(output_label, 1, 0)
        layout.addWidget(self.output_selector, 1, 1)
        layout.setColumnStretch(layout.columnCount(), 1)
        self.setLayout(layout)

    def get_observer(self):
        return self.observer_selector.currentText()

    def get_step_size(self):
        return int(self.observer_step_size_selector.currentText())

    def process(self, spectral_image):

        step_size = self.get_step_size()
        output_space = self.output_selector.currentText()
        if output_space == "XYZ":
            image = spectral_to_XYZ_using_cie_observer(spectral_image, step_size)
        elif output_space == "sRGB":
            image = spectral_to_RGB_using_cie_observer(spectral_image, step_size)

        return image