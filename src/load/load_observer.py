import pandas as pd
import numpy as np


def load_observer(min_wavelength=400, max_wavelength=700, step=10):
    # currently only takes the values at a given wavelength, can be improved
    # by giving eg. a weighted average
    data = pd.read_csv('./res/observer/CIE_xyz_1931_2deg.csv', index_col=0,
                       header=None, names=['L', 'M', 'S'])

    observer = np.zeros((int((max_wavelength - min_wavelength) / step) + 1, 3))

    for i, wavelength in enumerate(range(min_wavelength, max_wavelength + 1, step)):
        observer[i] = data.loc[wavelength].values

    return observer
