import numpy as np


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
