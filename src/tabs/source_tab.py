import os
from PyQt6 import QtWidgets, QtGui, QtCore
from src.data_loader.load_image import load_spectral_image
from src import MIN_WAVELENGTH, MAX_WAVELENGTH


class SourceTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout()
        self.spectral_image = None
        self.bands = None

        self.image_path_input = QtWidgets.QLineEdit()
        self.image_path_input.setText("./res/images/ARAD_1K_0098.mat")
        self.image_path_button = QtWidgets.QPushButton("Load Image")
        self.image_path_button.pressed.connect(self._choose_file)

        layout.addWidget(self.image_path_input, 0, 0)
        layout.addWidget(self.image_path_button, 0, 1)

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

        self._update_metadata()
        layout.addWidget(self.metadata_table, 1, 0, 1, 2)
        self.setLayout(layout)

    def _choose_file(self):
        start_dir = self.get_path()
        chosen = QtWidgets.QFileDialog().getOpenFileName(directory=start_dir)
        if chosen[0]:
            self.image_path_input.setText(chosen[0])

    def _update_metadata(self):
        # Set some data in the table
        self.metadata_table.setItem(0, 0,
                                    QtWidgets.QTableWidgetItem(os.path.basename(self.get_path())))
        w, h, d = ('-', '-', '-')
        value_type, value_min, value_max = ("", "", "")

        if self.spectral_image is not None:
            w, h, d = self.spectral_image.shape
            value_type = self.spectral_image.dtype.name
            value_min = self.spectral_image.min()
            value_max = self.spectral_image.max()
        self.metadata_table.setItem(1, 0, QtWidgets.QTableWidgetItem(f'{w} x {h}'))
        self.metadata_table.setItem(2, 0, QtWidgets.QTableWidgetItem(f'{d}'))
        self.metadata_table.setItem(3, 0, QtWidgets.QTableWidgetItem(f'{MIN_WAVELENGTH}nm'))
        self.metadata_table.setItem(4, 0, QtWidgets.QTableWidgetItem(f'{MAX_WAVELENGTH}nm'))
        self.metadata_table.setItem(5, 0, QtWidgets.QTableWidgetItem(f'{value_type}'))
        self.metadata_table.setItem(6, 0, QtWidgets.QTableWidgetItem(f'{value_min}'))
        self.metadata_table.setItem(7, 0, QtWidgets.QTableWidgetItem(f'{value_max}'))

    def get_path(self):
        return self.image_path_input.text()

    def load_image(self):
        image_path = self.get_path()
        try:
            self.spectral_image, self.bands = load_spectral_image(image_path)
            self._update_metadata()
        except OSError as e:
            print(e)
            return
