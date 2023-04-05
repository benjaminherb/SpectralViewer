import pandas as pd


def load_observer(step_size):
    data = pd.read_csv('./res/observer/CIE_xyz_1931_2deg.csv', index_col=0,
                       header=None)

    return data[::step_size].values, data[::step_size].index
