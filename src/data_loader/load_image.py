import os.path
import h5py
import numpy as np
import scipy.io
import spectral
import json
from src.util.spectral_image import SpectralImage
from src.data_loader.load_illuminants import update_custom_illuminant
import logging

log = logging.getLogger(__name__)


def load_spectral_image(path):
    # load spectral image and bands from a .mat file
    if path.endswith('.mat'):
        return _load_mat(path)

    if path.lower().endswith(('.hdr', '.raw')):
        directory = os.path.dirname(path)
        filename = get_basename(path)
        if os.path.exists(os.path.join(directory, f'{filename}_metadata.json')):
            return _load_dataset_raw(path)
        else:
            return _load_specim(path)


def _load_mat(path):
    mat = scipy.io.loadmat(path, struct_as_record=False, squeeze_me=True)
    spectral_image = mat['data']
    wavelengths = mat['wavelengths'].squeeze()

    metadata = {
        'Filename': os.path.basename(path),
        'Size': f"{spectral_image.shape[0]} x {spectral_image.shape[1]} px",
        'Spectral Bands': spectral_image.shape[2],
        'Spectral Range': f"{min(wavelengths)} - {max(wavelengths)} nm",
        'Data Type': spectral_image.dtype.name,
        'Value Range': f"{spectral_image.min():.2f} - {spectral_image.max():.2f}",
    }

    if 'metadata' in mat:
        file_metadata = mat.get('metadata')
        if hasattr(file_metadata, 'illumination') and file_metadata.illumination:
            update_custom_illuminant(wavelengths, file_metadata.illumination, 'File')
        metadata.update({
            'Date': file_metadata.date,
            'Integration Time': file_metadata.tint,
            'Mode': file_metadata.mode,
            'Original Value Range': f"{file_metadata.min} - {file_metadata.max}",
            'Exposure': file_metadata.exposure,
        })

    return SpectralImage(spectral_image, wavelengths, metadata)


def _load_hdf5(path):

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


def _load_dataset_raw(path):
    directory = os.path.dirname(path)
    file = get_basename(path)

    data_ref = spectral.io.envi.open(
        os.path.join(directory, file + ".hdr"),
        os.path.join(directory, file + ".raw"))

    dark_ref = spectral.io.envi.open(
        os.path.join(directory, file + "_dark.hdr"),
        os.path.join(directory, file + "_dark.raw"))

    white = None
    if os.path.exists(os.path.join(directory, file + "_whiteref.hdr")):
        whiteref = spectral.io.envi.open(
            os.path.join(directory, file + "_whiteref.hdr"),
            os.path.join(directory, file + "_whiteref.raw"))
        whiteref_dark = spectral.io.envi.open(
            os.path.join(directory, file + "_whiteref_dark.hdr"),
            os.path.join(directory, file + "_whiteref_dark.raw"))
        white = whiteref.load()
        white_dark = whiteref_dark.load()
        white = np.subtract(white, white_dark)
        white = white / (2 ** 12 - white_dark.mean())

    data = np.array(data_ref.load())
    dark = np.array(dark_ref.load())
    corrected = np.subtract(data, dark)
    corrected = corrected / (2 ** 12 - dark.mean())

    calibration_directory = './res/calibration/specim_iq'
    was_corrected = False
    if os.path.isdir(calibration_directory):
        calibration_data = spectral.io.envi.open(
            os.path.join(calibration_directory, "Radiometric_1x1.hdr"),
            os.path.join(calibration_directory, "Radiometric_1x1.cal"))
        corrected = corrected * np.array(calibration_data.load())
        if white is not None:
            white = white * np.array(calibration_data.load())
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
        'Corrected': was_corrected,
    }

    wavelengths = np.array(data_ref.bands.centers)
    if white is not None:
        file_metadata = {}
        with open(os.path.join(directory, f"{file}_metadata.json")) as mdf:
            file_metadata = json.load(mdf)
        wpos = file_metadata['white_patch']
        white = np.mean(white[wpos[0]:wpos[0]+wpos[2], wpos[1]:wpos[1]+wpos[3]], axis=(0, 1))
        update_custom_illuminant(wavelengths, white, 'File')

    corrected = np.rot90(corrected, 3)
    return SpectralImage(corrected, wavelengths, metadata, white=white)


def _load_specim(path):
    directory = os.path.dirname(path)
    file = get_basename(path)

    data_ref = spectral.io.envi.open(
        os.path.join(directory, file + ".hdr"),
        os.path.join(directory, file + ".raw"))

    dark_ref = spectral.io.envi.open(
        os.path.join(directory, "DARKREF_" + file + ".hdr"),
        os.path.join(directory, "DARKREF_" + file + ".raw"))

    data = np.array(data_ref.load())
    dark = np.array(dark_ref.load())
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

    corrected = np.rot90(corrected, 3)

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
        'Corrected': was_corrected,
    }
    wavelengths = np.array(data_ref.bands.centers)

    return SpectralImage(corrected, wavelengths, metadata)

def get_basename(path):
    file = os.path.basename(path)
    for snip in ('.hdr', '.raw', '.RAW', '.HDR', '_whiteref', '_dark',
                 'DARKREF_', 'WHITEDARKREF_', 'WHITEREF_'):
        file = file.replace(snip, "")
    return file