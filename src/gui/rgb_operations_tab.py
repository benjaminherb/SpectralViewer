from PyQt6 import QtWidgets
from src.gui.change_transfer_curve_module import ChangeTransferCurveModule


class RGBOperationsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.operations = []

        self.new_operation_selector = QtWidgets.QComboBox()
        self.new_operation_selector.addItem("Change transfer curve")
        self.add_new_operation_button = QtWidgets.QPushButton("Add")
        self.add_new_operation_button.pressed.connect(self._add_operation)
        self.add_layout = QtWidgets.QHBoxLayout()
        self.add_layout.addWidget(self.new_operation_selector)
        self.add_layout.addWidget(self.add_new_operation_button)

        self.operations_layout = QtWidgets.QVBoxLayout()

        self.layout = QtWidgets.QVBoxLayout()  # main layout
        self.layout.addLayout(self.add_layout)
        self.layout.addLayout(self.operations_layout)
        self.layout.addStretch()
        self.setLayout(self.layout)

        self.update_operations()

    def update_operations(self):
        for operation in self.operations:
            self.operations_layout.addWidget(operation)
        self.setLayout(self.layout)
        print("Update Operations")

    def _add_operation(self):
        new_widget = ChangeTransferCurveModule()
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
