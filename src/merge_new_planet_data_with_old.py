import pandas as pd


def merge_new_planet_data():
    # Read the CSV files
    df1 = pd.read_csv('/Users/johan/IdeaProjects/solsystem_modell//data/solsystem_data.csv')
    df2 = pd.read_csv('/Users/johan/IdeaProjects/solsystem_modell//data/solsystem_data_1750.csv')

    # Set 'Name' column as index for both dataframes
    df1.set_index('Name', inplace=True)
    df2.set_index('Name', inplace=True)

    # Update the values in df1 with the values from df2
    df1.update(df2)

    # Reset the index
    df1.reset_index(inplace=True)

    # Write the updated dataframe to the solsystem_data.csv file
    df1.to_csv('/Users/johan/IdeaProjects/solsystem_modell/data/solsystem_data.csv', index=False)

    df1 = df1[:-1]
    df1.to_csv('/Users/johan/IdeaProjects/solsystem_modell/data/solsystem_data_uten_neptun.csv', index=False)


if __name__ == '__main__':
    merge_new_planet_data()
