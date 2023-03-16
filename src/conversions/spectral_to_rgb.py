import numpy as np
from src.load.load_observer import load_observer


def spectral_to_rgb_using_bands(spectral_image, bands=(20, 13, 3)):
    return np.stack((spectral_image[:, :, bands[0]],
                     spectral_image[:, :, bands[1]],
                     spectral_image[:, :, bands[2]]), axis=2)


def spectral_to_rgb_using_cie_observer(spectral_image):
    observer = load_observer(400, 700, 10)
    pass