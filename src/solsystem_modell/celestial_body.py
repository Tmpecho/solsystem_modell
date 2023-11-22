from collections import deque
from dataclasses import dataclass
from typing import Optional

from src import config

import numpy as np


@dataclass
class CelestialBodyAppearance:
    """A class representing the appearance of a celestial body"""
    name: str
    color: tuple[int, int, int]
    radius: int


@dataclass
class CelestialBodyProperties:
    """A class representing the data of a celestial body"""
    mass: float
    x_pos: float
    y_pos: float
    velocity: float
    direction: float
    max_trail_length: int


# TODO: Make appearance.size relative to the size of the screen and the size of the planet
class CelestialBody:
    """A class representing a celestial body"""

    def __init__(self, appearance: 'CelestialBodyAppearance', celestial_body_data: 'CelestialBodyProperties') -> None:
        self.name = appearance.name
        self.color = appearance.color

        self.mass = celestial_body_data.mass
        if config.TO_SCALE:
            self.size = appearance.radius / config.AU * config.ZOOM * config.SCALE_FACTOR
        else:
            if self.mass > 0:
                self.size = config.DEFAULT_OBJECT_SIZE * np.log(self.mass) / config.SIZE_SCALING_FACTOR * config.ZOOM
            else:
                self.size = 0
        self.position = np.array([celestial_body_data.x_pos, celestial_body_data.y_pos], dtype=np.float64)
        self.velocity = np.array([celestial_body_data.velocity * np.cos(celestial_body_data.direction),
                                  celestial_body_data.velocity * np.sin(celestial_body_data.direction)],
                                 dtype=np.float64)
        self.max_trail_length = celestial_body_data.max_trail_length
        self.is_stationary = appearance.name == "Sun" and config.IS_SUN_STATIONARY

        self.label_surfaces = None
        self.time_since_last_trail_update = 0
        self.trail_update_interval = config.TRAIL_UPDATE_INTERVAL
        self.positions = deque(maxlen=10000)

    def calculate_gravitational_force(self, other: 'CelestialBody') -> np.ndarray:
        return CelestialBodyCalculator.calculate_gravitational_force(self, other)

    def calculate_distance(self, other: 'CelestialBody') -> float:
        return CelestialBodyCalculator.calculate_distance(self, other)

    def calculate_direction(self, other: 'CelestialBody') -> float:
        return CelestialBodyCalculator.calculate_direction(self, other)

    def calculate_vector(self, other: 'CelestialBody') -> np.ndarray:
        return CelestialBodyCalculator.calculate_vector(self, other)

    def update_position(self, delta_time: float = None):
        if not self.is_stationary:
            self.update_velocity(None, delta_time)
            self.update_position_based_on_velocity(delta_time)
            self.update_trail(delta_time)

    def update_velocity(self, other: Optional['CelestialBody'], delta_time: float):
        if other is not None and self.mass != 0:
            force = self.calculate_gravitational_force(other)
            acceleration = force / self.mass
            self.velocity += acceleration * delta_time

    def update_position_based_on_velocity(self, delta_time: float):
        self.position += self.velocity * delta_time

    def update_trail(self, delta_time: float):
        self.time_since_last_trail_update += delta_time / config.TIME_ACCELERATION
        if self.time_since_last_trail_update >= self.trail_update_interval:
            self.positions.append(self.position.copy())
            self.time_since_last_trail_update = 0

    def distance_to_sun(self, sun: 'CelestialBody') -> float:
        if self.name == "Sun":
            return 0
        return np.linalg.norm(self.position - sun.position)

    def velocity_norm(self) -> float:
        return np.linalg.norm(self.velocity)

    def render_name(self, font, sun: 'CelestialBody') -> None:
        distance = self.distance_to_sun(sun) / config.AU
        velocity_norm = self.velocity_norm()

        label_lines = [
            f"{self.name}",
            f"Dist: {distance:.6f} AU",
            f"Vel: {velocity_norm:.3f} m/s"
        ]

        self.label_surfaces = [font.render(line, True, config.WHITE) for line in label_lines]


class CelestialBodyCalculator:
    @staticmethod
    def calculate_vector(body1: 'CelestialBody', body2: 'CelestialBody') -> np.ndarray:
        """Calculate the vector from body1 to body2"""
        return body2.position - body1.position

    @staticmethod
    def calculate_direction(body1: 'CelestialBody', body2: 'CelestialBody') -> float:
        """Calculate the direction from body1 to body2"""
        vector = CelestialBodyCalculator.calculate_vector(body1, body2)
        return np.arctan2(vector[1], vector[0])

    @staticmethod
    def calculate_distance(body1: 'CelestialBody', body2: 'CelestialBody') -> float:
        """Calculate the distance between body1 and body2"""
        vector = CelestialBodyCalculator.calculate_vector(body1, body2)
        return np.linalg.norm(vector)

    @staticmethod
    def calculate_gravitational_force(body1: 'CelestialBody', body2: 'CelestialBody') -> np.ndarray:
        """Calculate the gravitational force between body1 and body2"""
        distance_vector = CelestialBodyCalculator.calculate_vector(body1, body2)
        force_distance = CelestialBodyCalculator.calculate_distance(body1, body2)
        if force_distance == 0:
            raise ZeroDivisionError("Distance between celestial bodies cannot be zero.")
        force_magnitude = config.GAMMA * body1.mass * body2.mass / force_distance ** 2
        force_direction = distance_vector / force_distance
        return force_magnitude * force_direction
