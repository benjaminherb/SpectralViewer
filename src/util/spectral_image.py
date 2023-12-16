import scipy
import numpy as np
import logging

log = logging.getLogger(__name__)


class SpectralImage:
    def __init__(self, data, wavelengths, metadata=None, white=None):
        # limit values to the visible spectrum (based on 1931 2° Observer)
        self.original_minimum_wavelength = wavelengths.min()
        self.original_maximum_wavelength = wavelengths.max()

        minimum_visible_value = wavelengths.searchsorted(360) - 1
        maximum_visible_value = wavelengths.searchsorted(1200)
        if minimum_visible_value == -1:
            minimum_visible_value = 0

        self.data = data[:, :, minimum_visible_value:maximum_visible_value]
        self.data = self.data / self.data.max()  # scale to 0-1
        self.wavelengths = wavelengths[minimum_visible_value:maximum_visible_value]
        self.metadata = metadata

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

    def rotate_90(self, rotation_count):
        self.data = np.rot90(self.data, rotation_count, (0, 1))

    def flip_horizontal(self):
        self.data = np.fliplr(self.data)

    def flip_vertical(self):
        self.data = np.flipud(self.data)
