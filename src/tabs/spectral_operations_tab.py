from PyQt6 import QtWidgets
from src.spectral_modules.resample_module import SpectralResampleModule
from src.spectral_modules.change_illuminant_module import ChangeIlluminantModule
from src.spectral_modules.filter_module import FilterModule
from src.spectral_modules.saturation_module import SaturationModule


class SpectralOperationsTab(QtWidgets.QWidget):

    resample_operation_id = 0
    change_illuminant_operation_id = 1
    filter_operation_id = 2
    saturation_operation_id = 3

    def __init__(self):
        super().__init__()
        self.operations = []

        self.new_operation_selector = QtWidgets.QComboBox()
        self.new_operation_selector.addItems(
            ["Resample image", "Change illuminant", "Apply color filter", "Change saturation"])
        self.add_new_operation_button = QtWidgets.QPushButton("Add operation")
        self.add_new_operation_button.pressed.connect(self._add_operation)
        self.add_operation_layout = QtWidgets.QHBoxLayout()
        self.add_operation_layout.addWidget(self.new_operation_selector, 3)
        self.add_operation_layout.addWidget(self.add_new_operation_button)
        self.add_operation_layout.setContentsMargins(0, 5, 0, 5)

        self.operations_layout = QtWidgets.QVBoxLayout()

        self.layout = QtWidgets.QVBoxLayout()  # main layout
        self.layout.addLayout(self.add_operation_layout)
        self.layout.addLayout(self.operations_layout)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def _add_operation(self, selected_operation_id=None):
        if not selected_operation_id:
            selected_operation_id = self.new_operation_selector.currentIndex()

        new_widget = None
        if selected_operation_id == self.resample_operation_id:
            new_widget = SpectralResampleModule()

        if selected_operation_id == self.change_illuminant_operation_id:
            new_widget = ChangeIlluminantModule()

        if selected_operation_id == self.filter_operation_id:
            new_widget = FilterModule()

        if selected_operation_id == self.saturation_operation_id:
            new_widget = SaturationModule()

        if not new_widget:
            return

        new_widget.navigation_clicked.connect(self.navigation_clicked)

        self.operations_layout.addWidget(new_widget)
        self.operations.append(new_widget)
        self.update()

    def navigation_clicked(self, widget, action):

        if action == "delete":
            self.operations_layout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
            self.update()
            return

        current_index = self.operations_layout.indexOf(widget)
        moved_index = current_index
        if action == "up":
            moved_index = current_index - 1
        elif action == "down":
            moved_index = current_index + 1
        else:
            return

        if moved_index in range(0, self.operations_layout.count()):
            upper_widget = self.operations_layout.itemAt(moved_index).widget()
            self.operations_layout.insertWidget(moved_index, widget)
            self.operations_layout.insertWidget(current_index, upper_widget)

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
