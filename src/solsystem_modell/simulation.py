import numpy as np
import pygame

from src import config
from src.solsystem_modell.utils import create_celestial_bodies


class Simulation:
    """
    The Simulation class represents a simulation of celestial bodies in a solar system.
     """

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
        pygame.display.set_caption('Planets Simulation')

        self.celestial_bodies = create_celestial_bodies(file_name)

        pygame.font.init()
        # noinspection PyTypeChecker
        self.font = pygame.font.SysFont(None, config.FONT_SIZE)

    def calculate_forces(self) -> dict:
        forces = {celestial_body: np.zeros(2, dtype=np.float64) for celestial_body in self.celestial_bodies}
        for i, celestial_body_i in enumerate(self.celestial_bodies):
            for celestial_body_j in self.celestial_bodies[i + 1:]:
                force = celestial_body_i.calculate_gravitational_force(celestial_body_j)
                forces[celestial_body_i] += force
                forces[celestial_body_j] -= force
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
