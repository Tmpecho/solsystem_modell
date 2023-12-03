from src.solsystem_modell.celestial_body import CelestialBody, CelestialBodyAppearance, CelestialBodyProperties
from src import config
import numpy as np
import csv


def create_celestial_bodies(sun_x: float, sun_y: float, file_name) -> list[CelestialBody]:
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
            x_pos = sun_x + distance * np.sin(direction)
            y_pos = sun_y + distance * np.cos(direction)
            max_trail_length = int(max_trail_length)

            # noinspection PyTypeChecker
            celestial_body_appearance = CelestialBodyAppearance(name, color, radius)
            celestial_body_properties = CelestialBodyProperties(mass, x_pos, y_pos,
                                                                velocity, direction, max_trail_length)
            celestial_body = CelestialBody(celestial_body_appearance, celestial_body_properties)
            planets.append(celestial_body)
    return planets
