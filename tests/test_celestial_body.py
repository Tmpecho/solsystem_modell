import unittest

import numpy as np

import src.config as config
import src.solsystem_modell.celestial_body as cb


class TestCelestialBody(unittest.TestCase):
    def setUp(self):
        self.earth = cb.CelestialBody(cb.CelestialBodyAppearance("Earth", (0, 0, 255), 5),
                                      cb.CelestialBodyProperties(5.9722e24, 1.496e11, 0, 29784.8, np.pi / 2, 800))
        self.sun = cb.CelestialBody(cb.CelestialBodyAppearance("Sun", (255, 255, 0), 10),
                                    cb.CelestialBodyProperties(1.98847e30, 0, 0, 0, 0, 100))
        self.null_body = cb.CelestialBody(cb.CelestialBodyAppearance("Null", (0, 0, 0), 0),
                                          cb.CelestialBodyProperties(0, 0, 0, 0, 0, 0))

    def test_calculate_force_when_distance_is_zero(self):
        self.earth.position = self.sun.position
        with self.assertRaises(ZeroDivisionError):
            self.earth.calculate_gravitational_force(self.sun)

    def test_calculate_distance_when_positions_are_same(self):
        self.earth.position = self.sun.position
        calculated_distance = self.earth.calculate_distance(self.sun)
        self.assertEqual(calculated_distance, 0)

    def test_update_position_when_velocity_is_zero(self):
        self.earth.velocity = np.zeros(2)
        initial_position = self.earth.position.copy()
        self.earth.update_position(1)
        self.assertTrue(np.array_equal(self.earth.position, initial_position))

    def test_update_velocity_when_force_is_zero(self):
        self.earth.mass = 0
        initial_velocity = self.earth.velocity.copy()
        self.earth.update_velocity(self.sun, 1)
        self.assertTrue(np.array_equal(self.earth.velocity, initial_velocity))

    def test_calculate_force(self):
        expected_force = config.GAMMA * self.earth.mass * self.sun.mass / self.earth.calculate_distance(self.sun) ** 2
        calculated_force = np.linalg.norm(self.earth.calculate_gravitational_force(self.sun))
        self.assertAlmostEqual(calculated_force, expected_force, places=5)

    def test_calculate_distance(self):
        expected_distance = np.sqrt(
            (self.earth.position[0] - self.sun.position[0]) ** 2
            + (self.earth.position[1] - self.sun.position[1]) ** 2)
        calculated_distance = self.earth.calculate_distance(self.sun)
        self.assertAlmostEqual(calculated_distance, expected_distance, places=5)

    def test_calculate_direction(self):
        expected_direction = np.arctan2(self.sun.position[1] - self.earth.position[1],
                                        self.sun.position[0] - self.earth.position[0])
        calculated_direction = self.earth.calculate_direction(self.sun)
        self.assertAlmostEqual(calculated_direction, expected_direction, places=5)

    def test_update_position(self):
        initial_position = self.earth.position.copy()
        self.earth.update_position(1)
        self.assertNotEqual(self.earth.position.all(), initial_position.all())

    def test_update_velocity(self):
        initial_velocity = self.earth.velocity.copy()
        self.earth.update_velocity(self.sun, 1)
        self.assertFalse(np.array_equal(self.earth.velocity, initial_velocity))

    def test_distance_to_sun(self):
        expected_distance = np.linalg.norm(self.earth.position - self.sun.position)
        calculated_distance = self.earth.distance_to_sun(self.sun)
        self.assertAlmostEqual(calculated_distance, expected_distance, places=5)

    def test_velocity_norm(self):
        expected_velocity_norm = np.linalg.norm(self.earth.velocity)
        calculated_velocity_norm = self.earth.velocity_norm()
        self.assertAlmostEqual(calculated_velocity_norm, expected_velocity_norm, places=5)

    def test_calculate_force_with_null_body(self):
        calculated_force = np.linalg.norm(self.earth.calculate_gravitational_force(self.null_body))
        self.assertEqual(calculated_force, 0)

    def test_calculate_distance_with_null_body(self):
        expected_distance = np.linalg.norm(self.earth.position)
        calculated_distance = self.null_body.calculate_distance(self.earth)
        self.assertAlmostEqual(calculated_distance, expected_distance, places=5)

    def test_update_position_of_null_body(self):
        initial_position = self.null_body.position.copy()
        self.null_body.update_position(1)
        self.assertTrue(np.array_equal(self.null_body.position, initial_position))

    def test_update_velocity_of_null_body(self):
        initial_velocity = self.null_body.velocity.copy()
        self.null_body.update_velocity(self.earth, 1)
        self.assertTrue(np.array_equal(self.null_body.velocity, initial_velocity))

    def test_distance_from_null_body_to_sun(self):
        expected_distance = np.linalg.norm(self.sun.position)
        calculated_distance = self.null_body.distance_to_sun(self.sun)
        self.assertAlmostEqual(calculated_distance, expected_distance, places=5)

    def test_velocity_norm_of_null_body(self):
        calculated_velocity_norm = self.null_body.velocity_norm()
        self.assertEqual(calculated_velocity_norm, 0)


if __name__ == '__main__':
    unittest.main()
