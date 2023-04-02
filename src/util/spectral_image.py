import scipy
import numpy as np


class SpectralImage:
    def __init__(self, data, wavelengths):
        print(type(data))
        print(type(wavelengths))
        self.data = np.array(data)
        self.wavelengths = np.array(wavelengths)

    def get_wavelengths(self):
        return self.wavelengths

    def get_minimum_wavelength(self):
        return self.wavelengths.min()

    def get_maximum_wavelength(self):
        return self.wavelengths.max()

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

    def interpolate_wavelengths(self, wavelengths, interpolation_method='linear'):
        interpolation_function = scipy.interpolate.interp1d(
            self.get_wavelengths(), self.data, kind=interpolation_method, axis=2,
            fill_value=0, bounds_error=False)

        return interpolation_function(wavelengths)

