import pandas as pd


def load_primaries(colorspace="sRGB"):
    try:
        return pd.read_csv(f'./res/colorspaces/{colorspace}.csv', index_col=0)
    except FileNotFoundError as e:
        raise Exception(f"Colorspace '{colorspace}' could not be found in ./res/colorspaces")
