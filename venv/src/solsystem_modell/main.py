from solsystem_modell import Simulation, Renderer
from plotter import plot_data
import modell_config as config

import pygame
import numpy as np
import cProfile


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def initialize_simulations() -> tuple:
    simulations = [Simulation() for _ in range(2)]
    renderers = [Renderer(sim) for sim in simulations]

    for sim, data_file in zip(simulations, ["solsystem_data.csv", "solsystem_data_uten_neptun.csv"]):
        sim.initialize_simulation(config.DATA_FILE_PATH_ROOT + data_file)

    return simulations, renderers


def update_simulations(simulations, delta_time) -> None:
    for sim in simulations:
        sim.elapsed_time += delta_time
        sim.update_planet_positions(delta_time)


def collect_data(simulations, sun_position) -> tuple:
    uranus_positions = [sim.get_planet_position("Uranus") for sim in simulations]

    if all(pos is not None for pos in uranus_positions):
        distances = [np.linalg.norm(pos - sun_position) for pos in uranus_positions]
        return simulations[0].elapsed_time, distances[0], distances[1]

    return None, None, None


def main() -> None:
    pygame.init()

    simulations, renderers = initialize_simulations()
    clock = pygame.time.Clock()
    sun_position = simulations[0].get_planet_position("Sun")
    time_data, distance_data1, distance_data2 = [], [], []

    while handle_events():
        delta_time = (clock.tick(240) / 1000.0) * config.TIME_ACCELERATION

        update_simulations(simulations, delta_time)

        renderers[0].draw_all()

        elapsed_time, distance1, distance2 = collect_data(simulations, sun_position)

        if elapsed_time is not None:
            time_data.append(elapsed_time)
            distance_data1.append(distance1)
            distance_data2.append(distance2)

    plot_data(time_data, distance_data1, distance_data2, ['Uranus with Neptune', 'Uranus without Neptune'])
    pygame.quit()


if __name__ == "__main__":
    cProfile.run("main()") if config.DEBUG_MODE else main()
