import numpy as np
from src.conversions.matrices import get_XYZ_to_RGB_matrix
from src.load.load_primaries import load_primaries


def XYZ_to_RGB(XYZ_image):
    primaries = load_primaries("sRGB")
    XYZ_to_RGB_matrix = get_XYZ_to_RGB_matrix(primaries)
    # RGB_image = np.apply_along_axis(XYZ_image.reshape(-1, 3) *  XYZ_to_RGB_matrix
    print(XYZ_to_RGB_matrix)
    RGB_image = np.apply_along_axis(lambda v: np.dot(v, XYZ_to_RGB_matrix.T), axis=2,
                                    arr=XYZ_image)
    return RGB_image.reshape(XYZ_image.shape)
