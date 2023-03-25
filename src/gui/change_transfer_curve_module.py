from PyQt6 import QtWidgets
from src.conversions.tristimulus import linear_to_sRGB, sRGB_to_linear


class ChangeTransferCurveModule(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.convert_label = QtWidgets.QLabel("Convert")

        self.input_selector = QtWidgets.QComboBox()
        self.input_selector.addItem("Linear")
        self.input_selector.addItem("sRGB")
        self.input_selector.setCurrentText("Linear")

        self.to_label = QtWidgets.QLabel("to")

        self.output_selector = QtWidgets.QComboBox()
        self.output_selector.addItem("Linear")
        self.output_selector.addItem("sRGB")
        self.output_selector.setCurrentText("sRGB")

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.convert_label)
        self.layout.addWidget(self.input_selector)
        self.layout.addWidget(self.to_label)
        self.layout.addWidget(self.output_selector)
        self.layout.addStretch()
        self.layout.addWidget(self.up_button)
        self.layout.addWidget(self.down_button)
        self.layout.addWidget(self.delete_button)
        self.setLayout(self.layout)

    def process(self, image):
        input_curve = self.input_selector.currentText()
        output_curve = self.output_selector.currentText()

        if input_curve == output_curve:
            return image

        if input_curve == "sRGB" and output_curve == "Linear":
            return sRGB_to_linear(image)

        if input_curve == "Linear" and output_curve == "sRGB":
            return linear_to_sRGB(image)

        return image
