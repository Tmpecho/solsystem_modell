import cProfile

import numpy as np
import pygame

import config as config
from src.solsystem_modell.plotter import plot_data
from src.solsystem_modell.renderer import Renderer
from src.solsystem_modell.simulation import Simulation
from src.collect_planet_data import collect_planet_data
from src.merge_new_planet_data_with_old import merge_new_planet_data


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def initialize_simulations() -> tuple:
    simulations = [Simulation() for _ in range(2)]
    renderers = [Renderer(sim) for sim in simulations]

    for sim, data_file in zip(simulations, ['solsystem_data.csv', 'solsystem_data_uten_neptun.csv']):
        sim.initialize_simulation(config.DATA_FILE_PATH_ROOT + data_file)

    return simulations, renderers


def update_simulations(simulations, delta_time) -> None:
    for sim in simulations:
        sim.elapsed_time += delta_time
        sim.update_planet_positions(delta_time)


# TODO: Add the ability to save data to a file
def collect_data(simulations, sun_position) -> tuple:
    uranus_positions = [sim.get_planet_position('Uranus') for sim in simulations]

    if all(pos is not None for pos in uranus_positions):
        distances = [np.linalg.norm(pos - sun_position) for pos in uranus_positions]
        return simulations[0].elapsed_time, distances[0], distances[1]

    return None, None, None


def run_simulation(simulations, renderers):
    clock = pygame.time.Clock()
    sun_position = simulations[0].get_planet_position('Sun')
    time_data, distance_data1, distance_data2 = [], [], []
    total_elapsed_time = 0

    while handle_events() and total_elapsed_time < config.MAX_SIMULATION_YEARS * 60 * 60 * 24 * 365.25:
        delta_time = (clock.tick(240) / 1000.0) * config.TIME_ACCELERATION
        total_elapsed_time += delta_time

        update_simulations(simulations, delta_time)

        if config.SHOW_GRAPHICAL_VIEW:
            renderers[0].draw_all()

        elapsed_time, distance1, distance2 = collect_data(simulations, sun_position)

        if elapsed_time is not None:
            time_data.append(elapsed_time)
            distance_data1.append(distance1)
            distance_data2.append(distance2)

    return time_data, distance_data1, distance_data2


def main() -> None:
    collect_planet_data()
    merge_new_planet_data()

    pygame.init()

    simulations, renderers = initialize_simulations()

    time_data, distance_data1, distance_data2 = run_simulation(simulations, renderers)

    plot_data(time_data, distance_data1, distance_data2, ['Uranus with Neptune', 'Uranus without Neptune'])

    pygame.quit()


if __name__ == '__main__':
    main()
