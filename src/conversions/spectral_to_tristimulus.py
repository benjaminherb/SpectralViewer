import numpy as np
from src.conversions.tristimulus import XYZ_to_RGB
from src.data_loader.load_observer import load_observer
import scipy


def spectral_to_rgb_using_bands(spectral_image, bands=(20, 13, 3)):
    return np.stack((spectral_image[:, :, bands[0]],
                     spectral_image[:, :, bands[1]],
                     spectral_image[:, :, bands[2]]), axis=2)


def spectral_to_XYZ_using_cie_observer(spectral_image, step_size):
    observer, wavelengths = load_observer(
        spectral_image.minimum_wavelength, spectral_image.maximum_wavelength, step_size)

    interpolation_function_array = scipy.interpolate.interp1d(
        spectral_image.get_wavelengths(), spectral_image.data, kind='linear', axis=2)

    upsampled_spectral_image = interpolation_function_array(wavelengths)

    X = np.dot(upsampled_spectral_image, observer[0, :])
    Y = np.dot(upsampled_spectral_image, observer[1, :])
    Z = np.dot(upsampled_spectral_image, observer[2, :])
    XYZ = np.stack((X, Y, Z), axis=2)
    return XYZ / XYZ.max()  # scale to 1


def spectral_to_RGB_using_cie_observer(spectral_image, step_size):
    XYZ_image = spectral_to_XYZ_using_cie_observer(spectral_image, step_size)
    RGB_image = XYZ_to_RGB(XYZ_image)

    return RGB_image
