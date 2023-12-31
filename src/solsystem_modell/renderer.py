import psutil
import pygame
from datetime import datetime, timedelta

from src import config


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
                    if celestial_body.name == 'Sun'), None)

        for celestial_body in self.simulation.celestial_bodies:
            self.draw_labels(celestial_body, sun)

        self.draw_debug_info()

        pygame.display.flip()

    def draw_debug_info(self):
        if config.DEBUG_MODE:
            real_time = self.simulation.elapsed_time / config.TIME_ACCELERATION
            debug_info = [
                f'--DEBUG MODE ON--',
                f'Simulation start date: {config.START_DATE}',
                f'Time Acceleration: {config.TIME_ACCELERATION}',
                f'Sun Stationary: {config.IS_SUN_STATIONARY}',
                f'Zoom: {config.ZOOM}',
                f'Number of Celestial Bodies: {len(self.simulation.celestial_bodies)}',
                f'CPU Usage: {psutil.cpu_percent()}%',
                f'Memory Usage: {psutil.virtual_memory().percent}%',
                f'Simulation time: {real_time:.1f} seconds',
                f'To Scale: {config.TO_SCALE}',
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
        years_elapsed = days_elapsed / 365.25
        return days_elapsed, years_elapsed

    def render_elapsed_time(self, days_elapsed: float, years_elapsed: float) -> tuple:
        start_date = datetime.strptime(config.START_DATE, '%Y-%m-%d')
        current_date = start_date + timedelta(days=int(days_elapsed))
        current_date_text = self.simulation.font.render(
            f"Current date: {current_date.strftime('%Y-%m-%d')}", True, config.WHITE)
        days_text = self.simulation.font.render(f'Elapsed Days: {int(days_elapsed)}', True, config.WHITE)
        years_text = self.simulation.font.render(f'Elapsed Years: {years_elapsed:.1f}', True, config.WHITE)
        return current_date_text, days_text, years_text

    def blit_elapsed_time(self, current_date_text: str, days_text: str, years_text: str) -> None:
        self.simulation.screen.blit(current_date_text, (10, 10))
        self.simulation.screen.blit(days_text, (10, 30))
        self.simulation.screen.blit(years_text, (10, 50))

    def print_time_elapsed(self) -> None:
        days_elapsed, years_elapsed = self.calculate_elapsed_time()
        current_date_text, days_text, years_text = self.render_elapsed_time(days_elapsed, years_elapsed)
        self.blit_elapsed_time(current_date_text, days_text, years_text)

    def calculate_position(self, celestial_body: 'CelestialBody', sun: 'CelestialBody') -> tuple:
        x = int(self.simulation.width / 2 + ((celestial_body.position[0] - sun.position[0]) /
                                             self.simulation.real_width) * self.simulation.width)
        y = int(self.simulation.height / 2 + ((celestial_body.position[1] - sun.position[1]) /
                                              self.simulation.real_height) * self.simulation.height)
        return x, y

    def draw_planets(self) -> None:
        sun = next((celestial_body for celestial_body in self.simulation.celestial_bodies
                    if celestial_body.name == 'Sun'), None)
        if sun is None:
            return

        for celestial_body in self.simulation.celestial_bodies:
            if len(celestial_body.positions) > 1:
                self.draw_trail(celestial_body, sun)

            x, y = self.calculate_position(celestial_body, sun)
            pygame.draw.circle(self.simulation.screen, celestial_body.color,
                               (x, y), celestial_body.size)

    def draw_labels(self, celestial_body: 'CelestialBody', sun: 'CelestialBody') -> None:
        if not config.DEBUG_MODE:
            return

        celestial_body.render_name(self.simulation.font, sun)

        x, y = self.calculate_position(celestial_body, sun)

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
