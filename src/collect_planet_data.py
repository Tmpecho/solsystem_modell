import csv
import os

import numpy as np
from astropy import coordinates as coord
from astropy import units as u
from astropy.time import Time
from astropy.wcs import WCS


# FIXME: Temporary solution, but it's wrong
def transform_data(pos, vel):
    # Convert the velocity to a CartesianDifferential instance
    vel = coord.CartesianDifferential(vel.x, vel.y, 0 * u.au / u.s)

    vel = vel.norm().to(u.m / u.s).value

    # Calculate the distance from the origin to the position
    dist = np.sqrt(pos.x ** 2 + pos.y ** 2).to(u.AU).value

    return dist, vel


def get_path():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(parent_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, 'solsystem_data_1750.csv')
    return file_path


def process_data(time, writer):
    for name in ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']:
        pos, vel = coord.get_body_barycentric_posvel(name, time)

        dist, vel = transform_data(pos, vel)

        angle = np.arctan2(pos.y, pos.x).value

        writer.writerow([name, f'{dist:.5f}', f'{vel:.5f}', f'{angle:.5f}'])


def main():
    coord.solar_system_ephemeris.set('jpl')

    time = Time('1830-01-01')

    file_path = get_path()

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Distance (AU)', 'Velocity (m/s)', 'Direction (radians)'])

        process_data(time, writer)


if __name__ == '__main__':
    main()
