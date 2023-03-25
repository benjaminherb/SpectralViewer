import numpy as np
from src.conversions.matrices import get_XYZ_to_RGB_matrix
from src.data_loader.load_primaries import load_primaries


def XYZ_to_RGB(XYZ_image):
    primaries = load_primaries("sRGB")
    XYZ_to_RGB_matrix = get_XYZ_to_RGB_matrix(primaries)
    RGB_image = np.dot(XYZ_image, XYZ_to_RGB_matrix.T)
    return RGB_image


def linear_to_sRGB(v):
    return ((v > 0.0031308) * (1.055 * np.power(v, (1 / 2.4)) - 0.055)
            + (v <= 0.0031308) * (v * 12.92))


def sRGB_to_linear(v):
    return ((v > 0.04045) * np.power((0.055 + v) / 1.055, 2.4)
            + (v <= 0.04045) * (v / 12.92))
