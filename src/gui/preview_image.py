from PyQt6 import QtWidgets, QtCore


class PreviewImage(QtWidgets.QLabel):
    mouse_moved = QtCore.pyqtSignal(int, int)
    mouse_clicked = QtCore.pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed,
                           QtWidgets.QSizePolicy.Policy.Fixed)

    def mouseMoveEvent(self, event):
        self.mouse_moved.emit(event.pos().x(), event.pos().y())
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        self.mouse_clicked.emit(event.pos().x(), event.pos().y())
        super().mouseMoveEvent(event)
