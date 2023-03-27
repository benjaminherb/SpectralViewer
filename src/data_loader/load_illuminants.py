import numpy as np
import pandas as pd
import scipy


def load_illuminant(illuminant="CIE D65", min_wavelength=400, max_wavelength=700, step_size=1):
    if illuminant == "CIE D65":
        filename = "CIE_std_illum_D65.csv"
    elif illuminant == "CIE D50":
        filename = "CIE_std_illum_D50.csv"
    elif illuminant == "CIE A":
        filename = "CIE_std_illum_A_1nm.csv"
    else:
        raise Exception(f"Illuminant '{illuminant}' could not be found in ./res/illuminants")

    data = pd.read_csv(f'./res/illuminants/{filename}', index_col=0, header=None)

    # return data.loc[400:700].values, np.arange(min_wavelength, max_wavelength+1, 1)

    values = int((max_wavelength - min_wavelength) / step_size) + 1

    # interpolate values
    wavelengths = np.linspace(min_wavelength, max_wavelength, values)
    interpolation_function = scipy.interpolate.interp1d(
        data.index.values, data.values, axis=0, kind='linear')
    illuminant = interpolation_function(wavelengths)

    return illuminant[:, 0] / 100, wavelengths
