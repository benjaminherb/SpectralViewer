import numpy as np
from src.conversions.tristimulus import XYZ_to_RGB
from src.data_loader.load_observer import load_observer


def spectral_to_rgb_using_bands(spectral_image, bands=(20, 13, 3)):
    return np.stack((spectral_image[:, :, bands[0]],
                     spectral_image[:, :, bands[1]],
                     spectral_image[:, :, bands[2]]), axis=2)


def spectral_to_XYZ_using_cie_observer(spectral_image):
    observer = load_observer(spectral_image.minimum_wavelength, spectral_image.maximum_wavelength,
                             spectral_image.depth())
    # X = np.apply_along_axis(lambda v: np.dot(v, observer[:, 0]), axis=2, arr=spectral_image)
    X = np.dot(spectral_image.data, observer[0, :])
    Y = np.dot(spectral_image.data, observer[1, :])
    Z = np.dot(spectral_image.data, observer[2, :])
    XYZ = np.stack((X, Y, Z), axis=2)
    return XYZ / XYZ.max()  # scale to 1


def spectral_to_RGB_using_cie_observer(spectral_image):
    XYZ_image = spectral_to_XYZ_using_cie_observer(spectral_image)
    RGB_image = XYZ_to_RGB(XYZ_image)

    return RGB_image
