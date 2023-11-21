import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def plot_data(time_data, distance_data1, distance_data2, labels):
    time_data = [t / (60 * 60 * 24 * 365.25) for t in time_data]
    distance_data1 = [d / 1000 for d in distance_data1]
    distance_data2 = [d / 1000 for d in distance_data2]

    difference_data = [abs(d1 - d2) for d1, d2 in zip(distance_data1, distance_data2)]

    data = pd.DataFrame({
        'Time (years)': time_data,
        f'{labels[0]} (km)': distance_data1,
        f'{labels[1]} (km)': distance_data2,
        'Difference (km)': difference_data
    })

    # sns.lineplot(data=data, x='Time (years)', y=f'{labels[0]} (km)')
    # sns.lineplot(data=data, x='Time (years)', y=f'{labels[1]} (km)')
    sns.lineplot(data=data, x='Time (years)', y='Difference (km)', linestyle='--')
    plt.legend(title='Uranus', loc='upper right', labels=[f'{label} (km)' for label in labels] + ['Difference (km)'])
    plt.title('Distances of Uranus with and without Neptune over Time')
    plt.show()
