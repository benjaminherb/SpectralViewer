import h5py
import numpy as np


def load_spectral_image(path):
    # load spectral image and bands from a .mat file
    with h5py.File(path, 'r') as mat:
        spectral_image = np.array(mat['cube']).T
        bands = None
        if 'bands' in mat:
            bands = np.array(mat['bands']).squeeze()
    return spectral_image, bands


def spectral_to_rgb(spectral_image, bands=(3, 13, 23)):
    return np.stack((spectral_image[:, :, bands[0]],
                     spectral_image[:, :, bands[1]],
                     spectral_image[:, :, bands[2]]), axis=2)
