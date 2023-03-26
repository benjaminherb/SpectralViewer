from PyQt6 import QtWidgets, QtGui, QtCore


class ObserverConversion(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        observer_label = QtWidgets.QLabel("Observer:")
        self.observer_selector = QtWidgets.QComboBox()
        self.observer_selector.addItems(["CIE 1931"])
        observer_label_2 = QtWidgets.QLabel("in")
        self.observer_step_size_selector = QtWidgets.QComboBox()
        self.observer_step_size_selector.addItems(["1", "2", "5", "10"])
        self.observer_step_size_selector.setCurrentText("10")
        observer_label_3 = QtWidgets.QLabel("nm steps")

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

    def get_output(self):
        return self.output_selector.currentText()

    def get_observer(self):
        return self.observer_selector.currentText()

    def get_step_size(self):
        return int(self.observer_step_size_selector.currentText())
