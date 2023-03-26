import pandas as pd
import numpy as np
import scipy


def load_observer(min_wavelength=400, max_wavelength=700, step_size=1):
    data = pd.read_csv('./res/observer/CIE_xyz_1931_2deg.csv', index_col=0,
                       header=None, names=['X', 'Y', 'Z'])

    # return data.loc[400:700].values, np.arange(min_wavelength, max_wavelength+1, 1)

    values = int((max_wavelength - min_wavelength)/step_size) + 1

    observer = np.zeros((3, values))

    # interpolate values
    wavelengths = np.linspace(min_wavelength, max_wavelength, values)
    for i in range(3):
        interpolation_function = scipy.interpolate.interp1d(
            data.index, data.iloc[:, i].values, kind='linear')
        observer[i] = interpolation_function(wavelengths)

    return observer, wavelengths
