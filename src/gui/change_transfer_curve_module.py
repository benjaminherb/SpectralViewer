from PyQt6 import QtWidgets


class ChangeTransferCurveModule(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.input_selector = QtWidgets.QComboBox()
        self.input_selector.addItem("Linear")

        self.output_selector = QtWidgets.QComboBox()
        self.output_selector.addItem("Linear")
        self.output_selector.addItem("sRGB")

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.input_selector)
        self.layout.addWidget(self.output_selector)
        self.layout.addStretch()
        self.layout.addWidget(self.up_button)
        self.layout.addWidget(self.down_button)
        self.layout.addWidget(self.delete_button)
        self.setLayout(self.layout)
