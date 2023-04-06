import numpy as np
from src.conversions.tristimulus import XYZ_to_RGB
from src.data_loader.load_observer import load_observer
from src.data_loader.load_camera import load_camera


def spectral_to_rgb_using_bands(spectral_image, bands=(20, 13, 3)):
    return np.stack((spectral_image.data[:, :, bands[0]],
                     spectral_image.data[:, :, bands[1]],
                     spectral_image.data[:, :, bands[2]]), axis=2)


def spectral_to_XYZ_using_cie_observer(spectral_image, step_size):
    observer, wavelengths = load_observer(step_size)
    resampled_spectral_image = spectral_image.interpolate_wavelengths(wavelengths, 'linear')

    X = np.dot(resampled_spectral_image, observer[:, 0])
    Y = np.dot(resampled_spectral_image, observer[:, 1])
    Z = np.dot(resampled_spectral_image, observer[:, 2])
    XYZ = np.stack((X, Y, Z), axis=2)
    return XYZ


def spectral_to_RGB_using_cie_observer(spectral_image, step_size):
    XYZ_image = spectral_to_XYZ_using_cie_observer(spectral_image, step_size)
    RGB_image = XYZ_to_RGB(XYZ_image)
    return RGB_image


def spectral_to_RGB_using_camera_response(spectral_image, camera_name, step_size):
    camera, wavelengths = load_camera(camera_name, step_size)
    resampled_spectral_image = spectral_image.interpolate_wavelengths(wavelengths, 'linear')
    R = np.dot(resampled_spectral_image, camera[:, 0])
    G = np.dot(resampled_spectral_image, camera[:, 1])
    B = np.dot(resampled_spectral_image, camera[:, 2])
    RGB = np.stack((R, G, B), axis=2)
    return RGB
