import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime, timedelta

import src.config as config


def plot_data(time_data, distance_data1, distance_data2, labels):
    start_date = datetime.strptime(config.START_DATE, '%Y-%m-%d')
    date_data = [start_date + timedelta(seconds=t) for t in time_data]

    distance_data1 = [d / 1000 for d in distance_data1]
    distance_data2 = [d / 1000 for d in distance_data2]

    difference_data = [abs(d1 - d2) for d1, d2 in zip(distance_data1, distance_data2)]

    data = pd.DataFrame({
        'Date': date_data,
        f'{labels[0]} (km)': distance_data1,
        f'{labels[1]} (km)': distance_data2,
        'Difference (km)': difference_data
    })

    # Calculate time elapsed
    time_elapsed = date_data[-1] - date_data[0]
    time_elapsed_str = f'Time elapsed: {time_elapsed.days} days'

    # Plot for positions
    plt.figure()
    sns.lineplot(data=data, x='Date', y=f'{labels[0]} (km)')
    sns.lineplot(data=data, x='Date', y=f'{labels[1]} (km)')
    plt.legend(title='Uranus', labels=[f'{label} (km)' for label in labels])
    plt.title('Distances of Uranus with and without Neptune over Time')
    plt.text(0.5, 0.02, time_elapsed_str, ha='center', va='center', transform=plt.gca().transAxes)
    plt.show()

    # Plot for difference
    plt.figure()
    sns.lineplot(data=data, x='Date', y='Difference (km)', linestyle='--')
    plt.legend(title='Uranus', labels=['Difference (km)'])
    plt.title('Difference in Distances of Uranus with and without Neptune over Time')
    plt.text(0.5, 0.02, time_elapsed_str, ha='center', va='center', transform=plt.gca().transAxes)
    plt.show()
