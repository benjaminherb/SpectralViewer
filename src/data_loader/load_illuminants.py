import pandas as pd
import scipy


def get_illuminants():
    return {
        'CIE D65': {'file': 'CIE_std_illum_D65.csv', 'name': ""},
        'CIE D50': {'file': 'CIE_std_illum_D50.csv', 'name': ""},
        'CIE A': {'file': 'CIE_std_illum_A_1nm.csv', 'name': ""},
        'CIE E': {'file': 'CIE_std_illum_E.csv', 'name': ""},
        'Eiko Halogen': {'file': 'Eiko_Solux_i1_4700k_tungsten_halogen.csv', 'name': ""},
        'Arri Compact 125W HMI': {'file': 'Arri_HMI_normalized_v2.csv',
                                  'name': 'Arri_Compact125W_HMI_Flood'},
        'Arri D5 1200W HMI': {'file': 'Arri_HMI_normalized_v2.csv',
                              'name': 'Arri_D5-1_1200W_HMI_Flood'},
        'Arri Daylight Compact 1200W HMI': {'file': 'Arri_HMI_normalized_v2.csv',
                                            'name': 'Arri_Daylight_Compact_1200W_HMI_Flood'},
        'Arri M40 2500W HMI': {'file': 'Arri_HMI_normalized_v2.csv',
                               'name': 'Arri_M40_2500W_HMI_52°_EVG-Max'},
    }


def get_illuminant_names():
    return list(get_illuminants().keys())


def load_illuminant(illuminant_name, wavelengths, interpolation_method='linear'):
    illuminant = get_illuminants()[illuminant_name]

    if not illuminant['name']:  # simple csv with only one illuminant
        data = pd.read_csv(f'./res/illuminants/{illuminant["file"]}', index_col=0, header=None)
    else:  # open film tools file with multiple illuminants per csv file
        data = pd.read_csv(f'./res/illuminants/{illuminant["file"]}',
                           index_col=0, header=0, delimiter=";").loc[illuminant['name']]
        data.index = data.index.astype(int)

    # pad with 1 to avoid changing the value when changing illuminants (or dividing by zero)
    interpolation_function = scipy.interpolate.interp1d(
        data.index.values, data.values, axis=0,
        kind=interpolation_method, fill_value=1, bounds_error=False)
    interpolated_illuminant = interpolation_function(wavelengths)

    # cie illuminants are usually scaled to 100 at 560nm
    interpolated_illuminant = interpolated_illuminant / interpolation_function(560)
    interpolated_illuminant = interpolated_illuminant.flatten()  # in case it is 2d not 3d

    return interpolated_illuminant
