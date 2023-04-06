import numpy as np
from src.data_loader.load_reflectances import load_reflectances
from src.data_loader.load_illuminants import load_illuminant
from src.data_loader.load_camera import load_camera
from src.data_loader.load_observer import load_observer
from src.data_loader.load_primaries import load_primaries


def get_RGB_to_XYZ_matrix(primaries):
    Xr, Yr, Zr = xy_to_XYZ(
        primaries['Red']['x'], primaries['Red']['y'], primaries['Red']['Y'])
    Xg, Yg, Zg = xy_to_XYZ(
        primaries['Green']['x'], primaries['Green']['y'], primaries['Green']['Y'])
    Xb, Yb, Zb = xy_to_XYZ(
        primaries['Blue']['x'], primaries['Blue']['y'], primaries['Blue']['Y'])
    Xw, Yw, Zw = xy_to_XYZ(
        primaries['Whitepoint']['x'], primaries['Whitepoint']['y'], primaries['Whitepoint']['Y'])

    XYZ_matrix = np.array([[Xr, Xg, Xb], [Yr, Yg, Yb], [Zr, Zg, Zb]])
    XwYwZw_vector = np.array([Xw, Yw, Zw])
    SrSgSb_vector = np.linalg.solve(XYZ_matrix, XwYwZw_vector)
    RGB_to_XYZ_matrix = XYZ_matrix * np.array([SrSgSb_vector, SrSgSb_vector, SrSgSb_vector]).T
    return RGB_to_XYZ_matrix


def get_XYZ_to_RGB_matrix(primaries):
    return np.linalg.inv(get_RGB_to_XYZ_matrix(primaries))


def xy_to_XYZ(x, y, Y):
    # http://www.brucelindbloom.com/index.html?Eqn_Spect_to_XYZ.html
    if y == 0:
        return 0, 0, 0
    X = x * Y / y
    Z = (1 - x - y) * Y / y
    return X, Y, Z


def get_camera_characterisation_matrix(camera_name, reflectance_set_name,
                                       camera_illuminant_name, reference_illuminant_name):

    camera, wavelengths = load_camera(camera_name, step_size=1)
    observer, observer_wavelengths = load_observer(step_size=1)

    reflectances = load_reflectances(reflectance_set_name, wavelengths)

    camera_illuminant = load_illuminant(camera_illuminant_name, wavelengths)
    camera_radiance = reflectances * camera_illuminant.reshape(-1, 1)
    RGB_camera = (camera_radiance[:, :, np.newaxis] * camera[:, np.newaxis, :]).sum(axis=0) / len(
        wavelengths)

    reference_illuminant = load_illuminant(reference_illuminant_name, wavelengths)
    reference_radiance = reflectances * reference_illuminant.reshape(-1, 1)
    XYZ_observer = (reference_radiance[:, :, np.newaxis] * observer[:, np.newaxis, :]).sum(
        axis=0) / len(wavelengths)
    primaries = load_primaries("sRGB")
    XYZ_to_RGB_matrix = get_XYZ_to_RGB_matrix(primaries)
    RGB_observer = np.dot(XYZ_observer, XYZ_to_RGB_matrix.T)

    # pseudo inverse
    matrix = np.linalg.lstsq(RGB_camera, RGB_observer, rcond=None)[0]
    return matrix
