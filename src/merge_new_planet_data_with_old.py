import pandas as pd

from src.solsystem_modell.utils import get_path


def merge_new_planet_data():
    data_file_path = get_path('solsystem_data.csv')
    new_data_file_path = get_path('intermediate_solsystem_data.csv')

    original_data = pd.read_csv(data_file_path)
    new_data = pd.read_csv(new_data_file_path)

    original_data.set_index('Name', inplace=True)
    new_data.set_index('Name', inplace=True)

    original_data.update(new_data)

    original_data.reset_index(inplace=True)
    original_data.to_csv(data_file_path, index=False)

    original_data = original_data[:-1]
    original_data.to_csv(data_file_path.replace('.csv', '_uten_neptun.csv'), index=False)
