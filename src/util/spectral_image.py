import numpy as np


class SpectralImage:
    def __init__(self, data, minimum_wavelength=400, maximum_wavelength=700):
        self.data = data
        self.minimum_wavelength = minimum_wavelength
        self.maximum_wavelength = maximum_wavelength

    def get_wavelength_step(self):
        return (self.maximum_wavelength - self.minimum_wavelength) / (self.depth() - 1)

    def get_dimension(self, dimension=-1):
        shape = self.data.shape
        if dimension in range(3):
            return shape[dimension]

        return self.data.shape

    def height(self):
        return self.get_dimension(0)

    def width(self):
        return self.get_dimension(1)

    def depth(self):
        return self.get_dimension(2)
