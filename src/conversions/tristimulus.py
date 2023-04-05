import numpy as np
from src.conversions.matrices import get_XYZ_to_RGB_matrix, get_RGB_to_XYZ_matrix
from src.data_loader.load_primaries import load_primaries
from src.data_loader.load_illuminants import get_illuminants, load_illuminant
from src.data_loader.load_observer import load_observer


def XYZ_to_RGB(XYZ_image):
    primaries = load_primaries("sRGB")
    XYZ_to_RGB_matrix = get_XYZ_to_RGB_matrix(primaries)
    RGB_image = np.dot(XYZ_image, XYZ_to_RGB_matrix.T)
    return RGB_image


def RGB_to_XYZ(RGB_image):
    primaries = load_primaries("sRGB")
    RGB_to_XYZ_matrix = get_RGB_to_XYZ_matrix(primaries)
    XYZ_image = np.dot(RGB_image, RGB_to_XYZ_matrix.T)
    return XYZ_image


def linear_to_sRGB(v):
    return ((v > 0.0031308) * (1.055 * np.power(v, (1 / 2.4)) - 0.055)
            + (v <= 0.0031308) * (v * 12.92))


def sRGB_to_linear(v):
    return ((v > 0.04045) * np.power((0.055 + v) / 1.055, 2.4)
            + (v <= 0.04045) * (v / 12.92))


def chromatic_adaptation(image, source_illuminant_name, destination_illuminant_name):
    # based on http://brucelindbloom.com/index.html?Eqn_ChromAdapt.html
    observer, wavelengths = load_observer(step_size=1)
    source_illuminant = load_illuminant(source_illuminant_name, wavelengths)
    destination_illuminant = load_illuminant(destination_illuminant_name, wavelengths)

    source_xyz = np.sum(observer * source_illuminant[:, np.newaxis], axis=0)
    source_xyz = source_xyz / source_xyz[1]  # scale to Y == 1
    destination_xyz = np.sum(observer * destination_illuminant[:, np.newaxis], axis=0)
    destination_xyz = destination_xyz / destination_xyz[1]
    domain_matrix = get_cone_response_domain_matrices("Bradford")
    inverse_domain_matrix = np.linalg.inv(domain_matrix)

    source_domain_vector = np.dot(domain_matrix, source_xyz)
    destination_domain_vector = np.dot(domain_matrix, destination_xyz)
    vector = destination_domain_vector / source_domain_vector

    matrix = np.dot(
        np.dot(inverse_domain_matrix,
               np.array([[vector[0], 0, 0], [0, vector[1], 0], [0, 0, vector[2]]])),
        domain_matrix)
    print(f"ChromAdapt: {matrix}")
    return np.dot(image, matrix)


def get_cone_response_domain_matrices(name):
    if name == "XYZ":
        return np.array([[1.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0],
                         [0.0, 0.0, 1.0]])
    elif name == "Bradford":
        return np.array([[0.8951, 0.2664, -0.1614],
                         [-0.7502, 1.7135, 0.0367],
                         [0.0389, -0.0685, 1.0296]])

    elif name == "Von Kries":
        return np.array([[0.40024, 0.7076, -0.08081],
                         [-0.2263, 1.16532, 0.0457],
                         [0.0, 0.0, 0.91822]])
