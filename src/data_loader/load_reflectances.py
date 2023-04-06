import pandas as pd
import scipy


def load_reflectances(name, wavelengths, interpolation_method="linear"):
    if not name == "Macbeth ColorChecker Classic":
        return

    data = pd.read_csv('./res/reflectances/macbeth_chart_reflectances.csv', index_col=0,
                       header=0)

    interpolation_function = scipy.interpolate.interp1d(
        data.index.values, data.values, axis=0,
        kind=interpolation_method, fill_value=0, bounds_error=False)
    interpolated_reflectances = interpolation_function(wavelengths)

    return interpolated_reflectances
