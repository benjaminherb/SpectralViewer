import os
from PyQt6 import QtWidgets
from src.data_loader.load_image import load_spectral_image


class SourceTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout()
        self.spectral_image = None

        # Input field
        self.image_path_input = QtWidgets.QLineEdit()
        self.image_path_input.setText("./res/images/ARAD_1K_0098.mat")
        self.image_path_button = QtWidgets.QPushButton("Load Image")
        self.image_path_button.pressed.connect(self._choose_file)

        # Metadata table
        self.metadata_table = QtWidgets.QTableWidget()
        self.metadata_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.metadata_table.setRowCount(8)
        self.metadata_table.setColumnCount(1)
        self.metadata_table.setVerticalHeaderLabels(
            ['Filename', 'Size', 'Depth', 'Min Wavelength', 'Max Wavelength',
             'Value Type', 'Min Value', 'Max Value'])
        self.metadata_table.verticalHeader().setMinimumWidth(100)
        self.metadata_table.horizontalHeader().setVisible(False)
        self.metadata_table.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Rotate & Flip
        self.rotate_label = QtWidgets.QLabel("Rotate")
        self.rotate_selector = QtWidgets.QComboBox()
        self.rotate_selector.addItems(["0°", "90°", "180°", "270°"])
        self.vertical_flip_selector = QtWidgets.QCheckBox("Flip vertically")
        self.vertical_flip_selector.setChecked(False)
        self.horizontal_flip_selector = QtWidgets.QCheckBox("Flip horizontally")
        self.horizontal_flip_selector.setChecked(False)
        rotate_flip_layout = QtWidgets.QHBoxLayout()
        rotate_flip_layout.addWidget(self.rotate_label)
        rotate_flip_layout.addWidget(self.rotate_selector)
        rotate_flip_layout.addWidget(self.horizontal_flip_selector)
        rotate_flip_layout.addWidget(self.vertical_flip_selector)
        rotate_flip_layout.addStretch()

        self._update_metadata()

        layout.addWidget(self.image_path_input, 0, 0)
        layout.addWidget(self.image_path_button, 0, 1)
        layout.addWidget(self.metadata_table, 1, 0, 1, 2)
        layout.addLayout(rotate_flip_layout, 2, 0, 1, 2)

        self.setLayout(layout)

    def _choose_file(self):
        start_dir = self.get_path()
        chosen = QtWidgets.QFileDialog().getOpenFileName(directory=start_dir)
        if chosen[0]:
            self.image_path_input.setText(chosen[0])

    def _update_metadata(self):
        # Set some data in the table
        self.metadata_table.setItem(
            0, 0, QtWidgets.QTableWidgetItem(os.path.basename(self.get_path())))
        w, h, d = ('-', '-', '-')
        value_type, value_min, value_max = ("", "", "")
        min_wavelength, max_wavelength = ("", "")

        if self.spectral_image is not None:
            w, h, d = self.spectral_image.data.shape
            value_type = self.spectral_image.data.dtype.name
            value_min = self.spectral_image.data.min()
            value_max = self.spectral_image.data.max()
            min_wavelength = self.spectral_image.get_minimum_wavelength()
            if self.spectral_image.original_minimum_wavelength != min_wavelength:
                min_wavelength = f"{min_wavelength} ({self.spectral_image.original_minimum_wavelength})"
            max_wavelength = self.spectral_image.get_maximum_wavelength()
            if self.spectral_image.original_maximum_wavelength != max_wavelength:
                max_wavelength = f"{max_wavelength} ({self.spectral_image.original_maximum_wavelength})"

        self.metadata_table.setItem(1, 0, QtWidgets.QTableWidgetItem(f'{w} x {h}'))
        self.metadata_table.setItem(2, 0, QtWidgets.QTableWidgetItem(f'{d}'))
        self.metadata_table.setItem(3, 0, QtWidgets.QTableWidgetItem(f'{min_wavelength} nm'))
        self.metadata_table.setItem(4, 0, QtWidgets.QTableWidgetItem(f'{max_wavelength} nm'))
        self.metadata_table.setItem(5, 0, QtWidgets.QTableWidgetItem(f'{value_type}'))
        self.metadata_table.setItem(6, 0, QtWidgets.QTableWidgetItem(f'{value_min}'))
        self.metadata_table.setItem(7, 0, QtWidgets.QTableWidgetItem(f'{value_max}'))

    def get_path(self):
        return self.image_path_input.text()

    def load_image(self):
        image_path = self.get_path()
        try:
            self.spectral_image = load_spectral_image(image_path)
            self._rotate_and_flip()
            self._update_metadata()

        except OSError as e:
            print(e)
            return

    def _rotate_and_flip(self):
        # the index indicates how often the image is rotated by 90°
        self.spectral_image.rotate_90(self.rotate_selector.currentIndex())

        if self.vertical_flip_selector.isChecked():
            self.spectral_image.flip_vertical()
        if self.horizontal_flip_selector.isChecked():
            self.spectral_image.flip_horizontal()

    def get_image(self):
        self.load_image()
        return self.spectral_image
