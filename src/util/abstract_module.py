from PyQt6 import QtWidgets, QtGui, QtCore


class AbstractModule(QtWidgets.QWidget):
    navigation_clicked = QtCore.pyqtSignal(QtWidgets.QWidget, str)

    # abstract module class
    def __init__(self):
        super().__init__()

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Window)

        self.up_button = QtWidgets.QPushButton("Up")
        self.up_button.clicked.connect(lambda: self.navigation_clicked.emit(self, "up"))
        self.down_button = QtWidgets.QPushButton("Down")
        self.down_button.clicked.connect(lambda: self.navigation_clicked.emit(self, "down"))
        self.delete_button = QtWidgets.QPushButton("Delete")
        self.delete_button.clicked.connect(lambda: self.navigation_clicked.emit(self, "delete"))

        self.navigation_layout = QtWidgets.QHBoxLayout()
        self.navigation_layout.addWidget(self.up_button)
        self.navigation_layout.addWidget(self.down_button)
        self.navigation_layout.addWidget(self.delete_button)

    def process(self, image):
        return image
