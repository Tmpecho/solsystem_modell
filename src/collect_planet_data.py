import csv
import os

import numpy as np
from astropy import coordinates as coord
from astropy import units as u
from astropy.time import Time
from astropy.wcs import WCS

import src.config as config
import src.solsystem_modell.utils as utils


def process_data(time, writer):
    for name in ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']:
        pos_eq, vel_eq = coord.get_body_barycentric_posvel(name, time)

        pos_ecl = coord.BarycentricMeanEcliptic(pos_eq)
        dist = pos_ecl.distance.to(u.AU).value
        angle = pos_ecl.lon.to(u.radian).value

        vel = vel_eq.norm().to(u.m / u.s).value

        writer.writerow([name, f'{dist:.5f}', f'{vel:.5f}', f'{angle:.5f}'])


def collect_planet_data():
    coord.solar_system_ephemeris.set('jpl')

    time = Time(config.START_DATE)

    file_path = utils.get_path('solsystem_data_1750.csv')

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Distance (AU)', 'Velocity (m/s)', 'Direction (radians)'])

        process_data(time, writer)
