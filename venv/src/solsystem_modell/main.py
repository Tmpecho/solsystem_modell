from solsystem_modell import Simulation, Renderer
import modell_config as config

import pygame

import cProfile


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def main() -> None:
    pygame.init()

    simulation = Simulation()
    simulation.initialize_simulation()

    render = Renderer(simulation)

    running = True
    clock = pygame.time.Clock()

    while running:
        running = handle_events()

        delta_time = (clock.tick(240) / 1000.0) * config.time_acceleration
        simulation.elapsed_time += delta_time

        render.draw_all()
        simulation.update_planet_positions(delta_time)

    pygame.quit()


if __name__ == "__main__":
    if not config.DEBUG_MODE:
        main()
    else:
        cProfile.run("main()")
