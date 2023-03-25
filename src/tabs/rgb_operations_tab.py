from PyQt6 import QtWidgets
from src.rgb_modules.change_transfer_curve_module import ChangeTransferCurveModule


class RGBOperationsTab(QtWidgets.QWidget):
    change_transfer_operation_id = 0

    def __init__(self):
        super().__init__()
        self.operations = []

        self.new_operation_selector = QtWidgets.QComboBox()
        self.new_operation_selector.addItem("Change transfer curve")
        self.add_new_operation_button = QtWidgets.QPushButton("Add operation")
        self.add_new_operation_button.pressed.connect(self._add_operation)
        self.add_operation_layout = QtWidgets.QHBoxLayout()
        self.add_operation_layout.addWidget(self.new_operation_selector, 3)
        self.add_operation_layout.addWidget(self.add_new_operation_button)
        print(self.add_operation_layout.getContentsMargins())
        self.add_operation_layout.setContentsMargins(0, 5, 0, 5)

        self.operations_layout = QtWidgets.QVBoxLayout()

        self.layout = QtWidgets.QVBoxLayout()  # main layout
        self.layout.addLayout(self.add_operation_layout)
        self.layout.addLayout(self.operations_layout)
        self.layout.addStretch()
        self.setLayout(self.layout)

        # default operations
        self._add_operation(self.change_transfer_operation_id)

    def _add_operation(self, selected_operation_id=None):
        if not selected_operation_id:
            selected_operation_id = self.new_operation_selector.currentIndex()

        new_widget = None
        if selected_operation_id == self.change_transfer_operation_id:
            new_widget = ChangeTransferCurveModule()

        if not new_widget:
            return

        new_widget.delete_button.pressed.connect(lambda: self._delete_operation(new_widget))
        new_widget.up_button.pressed.connect(lambda: self._move_operation(new_widget, -1))
        new_widget.down_button.pressed.connect(lambda: self._move_operation(new_widget, 1))

        self.operations_layout.addWidget(new_widget)
        self.operations.append(new_widget)
        self.update()

    def _delete_operation(self, widget):
        self.operations_layout.removeWidget(widget)
        widget.setParent(None)
        widget.deleteLater()
        self.update()

    def _move_operation(self, current_widget, move):
        current_index = self.operations_layout.indexOf(current_widget)
        moved_index = current_index + move
        if moved_index in range(0, self.operations_layout.count()):
            upper_widget = self.operations_layout.itemAt(moved_index).widget()
            self.operations_layout.insertWidget(moved_index, current_widget)
            self.operations_layout.insertWidget(current_index, upper_widget)

    def process(self, image):

        for index in range(self.operations_layout.count()):
            operation = self.operations_layout.itemAt(index).widget()
            if not operation:
                continue
            image = operation.process(image)

        return image
