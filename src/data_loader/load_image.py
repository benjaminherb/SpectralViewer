import os.path
import h5py
import numpy as np
import spectral
from src.util.spectral_image import SpectralImage


def load_spectral_image(path):
    # load spectral image and bands from a .mat file
    if path.endswith('.mat'):
        return _load_mat(path)

    if path.lower().endswith(('.hdr', '.raw')):
        return _load_specim(path)


def _load_mat(path):
    with h5py.File(path, 'r') as mat:
        spectral_image = np.array(mat['cube']).T
        bands = None
        if 'bands' in mat:
            bands = np.array(mat['bands']).squeeze()
    return SpectralImage(spectral_image, bands)


def _load_specim(path):
    directory = os.path.dirname(path)
    file = os.path.basename(path)[:-4]  # remove extension

    data_ref = spectral.io.envi.open(
        os.path.join(directory, file + ".hdr"),
        os.path.join(directory, file + ".raw"))

    # white_ref = spectral.io.envi.open(
    #    os.path.join(directory, "WHITEREF_" + file + ".hdr"),
    #    os.path.join(directory, "WHITEREF_" + file + ".raw"))

    dark_ref = spectral.io.envi.open(
        os.path.join(directory, "DARKREF_" + file + ".hdr"),
        os.path.join(directory, "DARKREF_" + file + ".raw"))

    # white = np.array(white_ref.load())
    dark = np.array(dark_ref.load())
    data = np.array(data_ref.load())

    corrected = np.subtract(data, dark)

    return SpectralImage(corrected, np.array(data_ref.bands.centers))
