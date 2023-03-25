from PyQt6 import QtWidgets, QtGui


class SpectralResampleModule(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setToolTip("Resample image to a lower spectral resolution using linear interpolation")

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Window)

        self.label_01 = QtWidgets.QLabel("Resample image to ")
        self.output_band_count = QtWidgets.QSpinBox()
        self.output_band_count.setValue(6)
        self.label_02 = QtWidgets.QLabel("bands")

        self.up_button = QtWidgets.QPushButton("Up")
        self.down_button = QtWidgets.QPushButton("Down")
        self.delete_button = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.label_01)
        self.layout.addWidget(self.output_band_count)
        self.layout.addWidget(self.label_02)
        self.layout.addStretch()
        self.layout.addWidget(self.up_button)
        self.layout.addWidget(self.down_button)
        self.layout.addWidget(self.delete_button)
        self.setLayout(self.layout)

    def process(self, image):
        output_bands = self.output_band_count.value()
        print(output_bands)
        return image
