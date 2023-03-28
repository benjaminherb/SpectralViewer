import pandas as pd
import scipy


def load_filter(filtername, wavelengths, interpolation_method='linear'):
    data = pd.read_csv(f'./res/filters/lee_filters.csv', index_col=0)

    filter = data[filtername]
    interpolation_function = scipy.interpolate.interp1d(
        filter.index.values, filter.values, axis=0, kind=interpolation_method)
    filter = interpolation_function(wavelengths)

    return filter
