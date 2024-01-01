import csv
import os

import numpy as np

from src import config
from src.solsystem_modell.celestial_body import CelestialBody, CelestialBodyAppearance, CelestialBodyProperties


def create_celestial_bodies(file_name) -> list[CelestialBody]:
    planets = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            name, color, radius, mass, distance, velocity, direction, max_trail_length = row
            color = tuple(map(int, color.strip("()").split(", ")))
            radius = int(radius) * 1000
            mass = float(mass)
            distance = float(distance) * config.AU
            velocity = float(velocity)
            direction = eval(direction.replace('pi', 'np.pi'))
            distance = float(distance)
            max_trail_length = int(max_trail_length)

            # noinspection PyTypeChecker
            celestial_body_appearance = CelestialBodyAppearance(name, color, radius)
            celestial_body_properties = CelestialBodyProperties(mass, distance,
                                                                velocity, direction, max_trail_length)
            celestial_body = CelestialBody(celestial_body_appearance, celestial_body_properties)
            planets.append(celestial_body)
    return planets


def polar_to_cartesian(r: float, theta: float) -> tuple:
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def get_path(file_name):
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(project_root, 'data', file_name)
    return data_dir
