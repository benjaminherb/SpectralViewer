from PyQt6 import QtWidgets, QtGui, QtCore


class ObserverConversion(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        observer_label = QtWidgets.QLabel("Observer:")
        self.observer_selector = QtWidgets.QComboBox()
        self.observer_selector.addItems(["CIE 1931"])
        output_label = QtWidgets.QLabel("Output:")
        self.output_selector = QtWidgets.QComboBox()
        self.output_selector.addItems(["sRGB", "XYZ"])

        layout = QtWidgets.QGridLayout()
        layout.addWidget(observer_label, 0, 0)
        layout.addWidget(self.observer_selector, 0, 1)
        layout.addWidget(output_label, 1, 0)
        layout.addWidget(self.output_selector, 1, 1)
        layout.setColumnStretch(layout.columnCount(), 1)
        self.setLayout(layout)

    def get_output(self):
        return self.output_selector.currentText()

    def get_observer(self):
        return self.observer_selector.currentText()
