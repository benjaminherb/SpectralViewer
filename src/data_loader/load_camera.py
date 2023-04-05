import pandas as pd


def get_cameras():
    return {
        'Arri Alexa': 'Arri_Alexa_nuke-arriraw-sdk.csv',
        'Baumer TXG50c': 'Baumer_TXG50c.csv',
        'Blackmagic Pocket 4K': 'BMD_PC4K.csv',
        'Canon 5D MK3': 'Canon_5DmkIII.csv',
        'Canon 6D': 'Canon_6D.csv',
        'GoPro Hero4 Black': 'GoPro_Hero4Black.csv',
        'Nikon D750': 'Nikon_D750.csv',
        'Nikon D800': 'Nikon_D800.csv',
        'PointGrey Flea3 FL3': 'PointGrey_Flea3_FL3-U3-32S2C.csv',
        'Sony A7R': 'Sony_A7r.csv',
    }


def get_camera_names():
    return list(get_cameras().keys())


def load_camera(camera_name, step_size=10):
    camera_file = get_cameras()[camera_name]
    data = pd.read_csv(f'./res/cameras/{camera_file}', header=0).transpose()
    return data[::step_size].values, data[::step_size].index.astype(int)
