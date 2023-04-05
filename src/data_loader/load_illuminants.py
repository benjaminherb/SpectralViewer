import pandas as pd
import numpy as np
import scipy


def get_illuminants():
    return {
        'CIE Illuminant D65': {'file': 'CIE_std_illum_D65.csv', 'name': ""},
        'CIE Illuminant D50': {'file': 'CIE_std_illum_D50.csv', 'name': ""},
        'CIE Illuminant A': {'file': 'CIE_std_illum_A_1nm.csv', 'name': ""},
        'CIE Illuminant E': {'file': 'CIE_std_illum_E.csv', 'name': ""},
        'Arri Compact 125W HMI': {'file': 'Arri_HMI_normalized_v2.csv',
                                  'name': 'Arri_Compact125W_HMI_Flood'},
        'Arri D5 1200W HMI': {'file': 'Arri_HMI_normalized_v2.csv',
                              'name': 'Arri_D5-1_1200W_HMI_Flood'},
        'Arri M40 2500W HMI': {'file': 'Arri_HMI_normalized_v2.csv',
                               'name': 'Arri_M40_2500W_HMI_52°_EVG-Max'},
        'Arri LoCaster LED 6500K': {'file': 'Arri_LED_normalized_v2.csv',
                                    'name': 'Arri_LoCaster_6500K_100%_Power'},
        'Arri LoCaster LED 3200K': {'file': 'Arri_LED_normalized_v2.csv',
                                    'name': 'Arri_LoCaster_3200K_100%_Power'},
        'Arri L7-C LED 6500K': {'file': 'Arri_LED_normalized_v2.csv',
                                'name': 'Arri_L7-C_LED_6500K_100%_Spot'},
        'Arri L7-C LED 3200K': {'file': 'Arri_LED_normalized_v2.csv',
                                'name': 'Arri_L7-C_LED_3200K_100%_Spot'},
        'Arri 2000 Plus Tungsten': {'file': 'Arri_TU_normalized_v2.csv',
                                    'name': 'Arri_2000Plus_TU_L1_Flood'},
        'Bron Kobold Lumax Fluorescent': {'file': 'Bron_Kobold_FL_normalized_v2.csv',
                                          'name': 'Bron_Kobold_Lumax_4x40W_L1_EVG-max55W_with_Eggcrate'},
        'Bron Kobold Dlf 575 HMI': {'file': 'Bron_Kobold_HMI_normalized_v2.csv',
                                    'name': 'Kobold_Dlf_575_HMI_Flood_EVG-Min'},
        'CMT Kinoflo KF55 Fluorescent': {'file': 'CMT_Kinoflo_FL_normalized_v2.csv',
                                         'name': 'CMT_Kinoflo_4feet4bank_L1_KF55_FL_EVG-4feet_no_Eggcrate'},
        'CMT Kinoflo KF32 Fluorescent': {'file': 'CMT_Kinoflo_FL_normalized_v2.csv',
                                         'name': 'CMT_Kinoflo_4feet4bank_L2_KF32_FL_EVG-4feet_no_Eggcrate'},
        'Dedolight Aspheric2 3400 Tungsten': {'file': 'Dedolight_TU_normalized_v2.csv',
                                              'name': 'Dedolight_Aspheric2_TU_L1_3400K_Flood'},
        'Dedolight Aspheric2 3200 Tungsten': {'file': 'Dedolight_TU_normalized_v2.csv',
                                              'name': 'Dedolight_Aspheric2_TU_L1_3200K_Flood'},
        'Eiko Halogen': {'file': 'Eiko_Solux_i1_4700k_tungsten_halogen.csv', 'name': ""},
    }


def get_illuminant_names():
    return list(get_illuminants().keys())


def load_illuminant(illuminant_name, wavelengths=None, interpolation_method='linear'):
    illuminant = get_illuminants()[illuminant_name]

    if not illuminant['name']:  # simple csv with only one illuminant
        data = pd.read_csv(f'./res/illuminants/{illuminant["file"]}', index_col=0, header=None)
    else:  # open film tools file with multiple illuminants per csv file
        data = pd.read_csv(f'./res/illuminants/{illuminant["file"]}',
                           index_col=0, header=0, delimiter=";").loc[illuminant['name']]
        data.index = data.index.astype(int)

    if wavelengths is None:
        return np.array(data).flatten()

    # pad with 1 to avoid changing the value when changing illuminants (or dividing by zero)
    interpolation_function = scipy.interpolate.interp1d(
        data.index.values, data.values, axis=0,
        kind=interpolation_method, fill_value=1, bounds_error=False)
    interpolated_illuminant = interpolation_function(wavelengths)

    # cie illuminants are usually scaled to 100 at 560nm
    interpolated_illuminant = interpolated_illuminant / interpolation_function(560)
    interpolated_illuminant = interpolated_illuminant.flatten()  # in case it is 2d not 3d

    return interpolated_illuminant
