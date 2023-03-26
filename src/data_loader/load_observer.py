import pandas as pd
import numpy as np
import scipy


def load_observer(min_wavelength=400, max_wavelength=700, values=31):
    # currently only takes the values at a given wavelength, can be improved
    # by giving eg. a weighted average
    data = pd.read_csv('./res/observer/CIE_xyz_1931_2deg.csv', index_col=0,
                       header=None, names=['X', 'Y', 'Z'])

    observer = np.zeros((3, values))

    # interpolate values
    wavelengths = np.linspace(min_wavelength, max_wavelength, values)
    for i in range(3):
        interpolation_function = scipy.interpolate.interp1d(
            data.index, data.iloc[:, i].values, kind='linear')
        observer[i] = interpolation_function(wavelengths)

    return observer
