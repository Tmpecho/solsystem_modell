import os
import numpy as np
import csv
import warnings
from erfa import ErfaWarning
from astropy import coordinates as coord
from astropy import units
from astropy.time import Time

import config


# TODO: Convert measurments to correct format
def main():
    coord.solar_system_ephemeris.set('jpl')

    # Suppress ERFA warnings
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=ErfaWarning)
        time = Time('1750-01-01')

    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(parent_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, 'solsystem_data_1750.csv')

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Distance (AU)', 'Velocity (m/s)', 'Direction (radians)'])

        for name in ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']:
            pos, vel = coord.get_body_barycentric_posvel(name, time)

            dist = pos - coord.get_body_barycentric_posvel('sun', time)[0]
            angle = np.arctan2(dist.y, dist.x)

            print(angle)

            writer.writerow(f'{name},{dist.norm():.3f},{vel:.1f},{angle:.3f}\n')


if __name__ == '__main__':
    main()
