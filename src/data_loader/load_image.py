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

    metadata = {
        'Filename': os.path.basename(path),
        'Size': f"{spectral_image.shape[0]} x {spectral_image.shape[1]} px",
        'Spectral Bands': spectral_image.shape[2],
        'Spectral Range': f"{min(bands)} - {max(bands)} nm",
        'Data Type': spectral_image.dtype.name,
        'Value Range': f"{spectral_image.min()} - {spectral_image.max()}",
    }

    return SpectralImage(spectral_image, bands, metadata)


def _load_specim(path):
    directory = os.path.dirname(path)
    file = os.path.basename(path)[:-4]  # remove extension

    data_ref = spectral.io.envi.open(
        os.path.join(directory, file + ".hdr"),
        os.path.join(directory, file + ".raw"))

    dark_ref = spectral.io.envi.open(
        os.path.join(directory, "DARKREF_" + file + ".hdr"),
        os.path.join(directory, "DARKREF_" + file + ".raw"))

    # white = np.array(white_ref.load())
    dark = np.array(dark_ref.load())
    data = np.array(data_ref.load())

    corrected = np.subtract(data, dark)

    corrected = corrected / (2 ** 12 - dark.mean())

    calibration_directory = './res/calibration/specim_iq'
    was_corrected = False
    if os.path.isdir(calibration_directory):
        calibration_data = spectral.io.envi.open(
            os.path.join(calibration_directory, "Radiometric_1x1.hdr"),
            os.path.join(calibration_directory, "Radiometric_1x1.cal"))
        corrected = corrected * np.array(calibration_data.load())
        was_corrected = True

    metadata = {
        'Filename': file,
        'Size': f"{data.shape[0]} x {data.shape[1]} px",
        'Spectral Bands': data.shape[2],
        'Spectral Range': f"{min(data_ref.bands.centers)} - {max(data_ref.bands.centers)} nm",
        'Data Type': data_ref.metadata.get('data type') + " bit",
        'Value Range': f"{data.min()} - {data.max()}",
        'Mean Black Value': dark.mean(),
        'Integration Time': data_ref.metadata.get('tint') + " ms",
        'Date': data_ref.metadata.get('acquisition date'),
    }
    return SpectralImage(corrected, np.array(data_ref.bands.centers), metadata)
