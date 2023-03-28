import numpy as np
import scipy


class SpectralImage:
    def __init__(self, data, minimum_wavelength=400, maximum_wavelength=700):
        self.data = data
        self.minimum_wavelength = minimum_wavelength
        self.maximum_wavelength = maximum_wavelength

    def get_wavelengths(self):
        return np.linspace(self.minimum_wavelength, self.maximum_wavelength, self.depth())

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

    def interpolate_wavelengths(self, wavelengths, interpolation_method='linear'):
        interpolation_function_array = scipy.interpolate.interp1d(
            self.get_wavelengths(), self.data, kind=interpolation_method, axis=2)
        upsampled_spectral_image = interpolation_function_array(wavelengths)

        return upsampled_spectral_image
