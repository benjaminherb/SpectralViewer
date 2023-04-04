import pandas as pd
import scipy


def get_filter_names():
    return ["Rose Pink", "Lavender Tint", "Medium Bastard Amber", "Pale Yellow",
            "Dark Salmon", "Pale Amber Gold", "Medium Yellow", "Straw Tint",
            "Deep Straw", "Surprise Peach", "Fire", "Medium Amber", "Gold Amber",
            "Dark Amber", "Scarlet", "Sunset Red", "Bright Red", "Medium Red",
            "Plasa Red", "Light Pink", "Medium Pink", "Pink Carnation", "Dark Magenta",
            "Rose Purple", "Light Lavender", "Paler Lavender", "Lavender", "Mist Blue",
            "Pale Blue", "Sky Blue"]


def load_filter(filtername, wavelengths, interpolation_method='linear'):
    data = pd.read_csv(f'./res/filters/lee_filters.csv', index_col=0)

    filter_data = data[filtername]
    interpolation_function = scipy.interpolate.interp1d(
        filter_data.index.values, filter_data.values, axis=0,
        kind=interpolation_method, fill_value=0, bounds_error=False)
    filter_data = interpolation_function(wavelengths)

    return filter_data
