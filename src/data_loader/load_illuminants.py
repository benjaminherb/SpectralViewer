import pandas as pd
import scipy


def get_illuminant_names() -> list:
    return ['CIE D65', 'CIE D50', 'CIE A', 'CIE E', 'Eiko Halogen']


def load_illuminant(illuminant, wavelengths, interpolation_method='linear'):
    if illuminant == "CIE D65":
        filename = "CIE_std_illum_D65.csv"
    elif illuminant == "CIE D50":
        filename = "CIE_std_illum_D50.csv"
    elif illuminant == "CIE A":
        filename = "CIE_std_illum_A_1nm.csv"
    elif illuminant == "CIE E":
        filename = "CIE_std_illum_E.csv"
    elif illuminant == "Eiko Halogen":
        filename = "Eiko_Solux_i1_4700k_tungsten_halogen.csv"
    else:
        raise Exception(f"Illuminant '{illuminant}' could not be found in ./res/illuminants")

    data = pd.read_csv(f'./res/illuminants/{filename}', index_col=0, header=None)

    # pad with 1 to avoid changing the value when changing illuminants (or dividing by zero)
    interpolation_function = scipy.interpolate.interp1d(
        data.index.values, data.values, axis=0,
        kind=interpolation_method, fill_value=1, bounds_error=False)
    illuminant = interpolation_function(wavelengths)

    # cie illuminants are usually scaled to 100 at 560nm
    value_at_560nm = interpolation_function(560)

    return illuminant[:, 0] / value_at_560nm
