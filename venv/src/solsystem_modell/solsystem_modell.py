from collections import deque
from dataclasses import dataclass
from typing import Optional
import psutil
import csv

import numpy as np
import pygame

import modell_config as config


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


# TODO: Multithread two versions of the simulation, one with Neptune and one without
# TODO: Graph distance between Uranus and Uranus without Neptune
class Simulation:
    """A class representing the simulation"""
    def __init__(self) -> None:
        self.celestial_bodies = []
        self.screen = None
        self.width = None
        self.height = None
        self.real_width = None
        self.real_height = None
        self.font = None
        self.elapsed_time = 0

    def initialize_simulation(self, file_name) -> None:
        scale = config.AU / 10
        self.width, self.height = config.SIMULATION_WIDTH, config.SIMULATION_HEIGHT
        self.real_width, self.real_height = self.width / config.ZOOM * scale, self.height / config.ZOOM * scale

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE)
        pygame.display.set_caption("Planets Simulation")

        sun_x, sun_y = self.real_width / 2, self.real_height / 2
        self.celestial_bodies = create_celestial_bodies(sun_x, sun_y, file_name)

        pygame.font.init()
        # noinspection PyTypeChecker
        self.font = pygame.font.SysFont(None, config.FONT_SIZE)

    def calculate_forces(self) -> dict:
        forces = {celestial_body: np.zeros(2, dtype=np.float64) for celestial_body in self.celestial_bodies}
        n = len(self.celestial_bodies)
        for i in range(n):
            for j in range(i + 1, n):
                force = self.celestial_bodies[i].calculate_gravitational_force(self.celestial_bodies[j])
                forces[self.celestial_bodies[i]] += force
                forces[self.celestial_bodies[j]] -= force
        return forces

    def update_planet_velocity(self, forces: dict, delta_time: float) -> None:
        for celestial_body in self.celestial_bodies:
            if not celestial_body.is_stationary:
                celestial_body.velocity += forces[celestial_body] / celestial_body.mass * delta_time

    def update_planet_position(self, delta_time: float) -> None:
        for celestial_body in self.celestial_bodies:
            if not celestial_body.is_stationary:
                celestial_body.update_position(delta_time)

    def update_trail(self, delta_time: float) -> None:
        for celestial_body in self.celestial_bodies:
            celestial_body.time_since_last_trail_update += delta_time / config.TIME_ACCELERATION
            if celestial_body.time_since_last_trail_update >= celestial_body.trail_update_interval:
                celestial_body.positions.append(celestial_body.position.copy())
                celestial_body.time_since_last_trail_update = 0

    def update_planet_positions(self, delta_time: float) -> None:
        forces = self.calculate_forces()
        self.update_planet_velocity(forces, delta_time)
        self.update_planet_position(delta_time)
        self.update_trail(delta_time)

    def get_planet_position(self, planet_name):
        for celestial_body in self.celestial_bodies:
            if celestial_body.name == planet_name:
                return celestial_body.position
        return None


class Renderer:
    """A class for rendering the simulation

    :param simulation: The simulation to render
    """
    def __init__(self, simulation: 'Simulation') -> None:
        self.simulation = simulation

    def draw_all(self) -> None:
        self.simulation.screen.fill(config.BLACK)
        self.print_time_elapsed()
        self.draw_planets()

        sun = next((celestial_body for celestial_body in self.simulation.celestial_bodies
                    if celestial_body.name == "Sun"), None)

        for celestial_body in self.simulation.celestial_bodies:
            self.draw_labels(celestial_body, sun)

        self.draw_debug_info()

        pygame.display.flip()

    def draw_debug_info(self):
        if config.DEBUG_MODE:
            real_time = self.simulation.elapsed_time / config.TIME_ACCELERATION
            debug_info = [
                f"--DEBUG MODE ON--",
                f"Time Acceleration: {config.TIME_ACCELERATION}",
                f"Sun Stationary: {config.IS_SUN_STATIONARY}",
                f"Zoom: {config.ZOOM}",
                f"Number of Celestial Bodies: {len(self.simulation.celestial_bodies)}",
                f"CPU Usage: {psutil.cpu_percent()}%",
                f"Memory Usage: {psutil.virtual_memory().percent}%",
                f"Simulation time: {real_time:.1f} seconds",
                f"To Scale: {config.TO_SCALE}",
            ]

            debug_surfaces = [self.simulation.font.render(info, True, config.WHITE) for info in debug_info]

            x, y = self.simulation.width - 20, 20
            line_height = self.simulation.font.get_linesize()

            for surface in debug_surfaces:
                text_rect = surface.get_rect(topright=(x, y))
                self.simulation.screen.blit(surface, text_rect)
                y += line_height

    def calculate_elapsed_time(self) -> tuple:
        days_elapsed = self.simulation.elapsed_time / (60 * 60 * 24)
        years_elapsed = days_elapsed / 365
        return days_elapsed, years_elapsed

    def render_elapsed_time(self, days_elapsed: float, years_elapsed: float) -> tuple:
        days_text = self.simulation.font.render(f'Days: {int(days_elapsed)}', True, config.WHITE)
        years_text = self.simulation.font.render(f'Years: {years_elapsed:.1f}', True, config.WHITE)
        return days_text, years_text

    def blit_elapsed_time(self, days_text: str, years_text: str) -> None:
        self.simulation.screen.blit(days_text, (10, 10))
        self.simulation.screen.blit(years_text, (10, 30))

    def print_time_elapsed(self) -> None:
        days_elapsed, years_elapsed = self.calculate_elapsed_time()
        days_text, years_text = self.render_elapsed_time(days_elapsed, years_elapsed)
        self.blit_elapsed_time(days_text, years_text)

    def draw_planets(self) -> None:
        sun = next((celestial_body for celestial_body in self.simulation.celestial_bodies
                    if celestial_body.name == "Sun"), None)
        if sun is None:
            return

        for celestial_body in self.simulation.celestial_bodies:
            if len(celestial_body.positions) > 1:
                self.draw_trail(celestial_body, sun)

            sun_x, sun_y = self.simulation.width // 2, self.simulation.height // 2

            x = sun_x + int(((celestial_body.position[0] - sun.position[0])
                             / self.simulation.real_width) * self.simulation.width)
            y = sun_y + int(((celestial_body.position[1] - sun.position[1])
                             / self.simulation.real_height) * self.simulation.height)
            pygame.draw.circle(self.simulation.screen, celestial_body.color,
                               (x, y), celestial_body.size)

    def draw_labels(self, celestial_body: 'CelestialBody', sun: 'CelestialBody') -> None:
        if not config.DEBUG_MODE:
            return

        celestial_body.render_name(self.simulation.font, sun)

        x = int((celestial_body.position[0] / self.simulation.real_width) * self.simulation.width)
        y = int((celestial_body.position[1] / self.simulation.real_height) * self.simulation.height)

        line_height = self.simulation.font.get_linesize()
        for label_surface in celestial_body.label_surfaces:
            self.simulation.screen.blit(label_surface, (x + 5, y + 5))
            y += line_height

    def draw_trail(self, celestial_body: 'CelestialBody', sun: 'CelestialBody') -> None:
        sun_x, sun_y = self.simulation.width // 2, self.simulation.height // 2

        points = ((sun_x + int(((pos[0] - sun.position[0]) / self.simulation.real_width) * self.simulation.width),
                   sun_y + int(((pos[1] - sun.position[1]) / self.simulation.real_height) * self.simulation.height))
                  for index, pos in enumerate(celestial_body.positions) if index % config.LINE_SKIP_FACTOR == 0)

        points_list = list(points)

        if len(points_list) >= 2:
            pygame.draw.lines(self.simulation.screen, config.WHITE, False, points_list, 1)


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


def create_celestial_bodies(sun_x: float, sun_y: float, file_name) -> list[CelestialBody]:
    planets = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            name, color, radius, mass, x_pos, y_pos, velocity, direction, max_trail_length = row
            color = tuple(map(int, color.strip("()").split(", ")))
            radius = int(radius)
            mass = float(mass)
            x_pos = eval(x_pos.replace('sun_x', str(sun_x)).replace('AU', 'config.AU'))
            y_pos = eval(y_pos.replace('sun_y', str(sun_y)))
            velocity = float(velocity)
            direction = eval(direction.replace('pi', 'np.pi'))
            max_trail_length = int(max_trail_length)

            # noinspection PyTypeChecker
            celestial_body_appearance = CelestialBodyAppearance(name, color, radius)
            celestial_body_properties = CelestialBodyProperties(mass, x_pos, y_pos,
                                                                velocity, direction, max_trail_length)
            celestial_body = CelestialBody(celestial_body_appearance, celestial_body_properties)
            planets.append(celestial_body)
    return planets
