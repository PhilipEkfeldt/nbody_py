from astropy import constants as const
import numpy as np


def gravity(positions, masses, dimensions=3):
    if dimensions == 3:
        p = np.tile(positions[:, np.newaxis, :], (1, positions.shape[0], 1))
        diff = np.transpose(p, (1, 0, 2)) - p
        dist = np.linalg.norm(diff, axis=2)
        directions = diff / dist[:, :, np.newaxis]
        directions = np.nan_to_num(directions, copy=True, nan=0)
        # print("Dist: ", dist)
        # print("Directions: ", directions)
        # print(const.G)
        # print("Mass : ", masses)
        force_mag = const.G * np.outer(masses, masses) / dist ** 2
        force_mag[force_mag == np.inf] = 0
        # print("FM: ", force_mag)
        forces = force_mag[:, :, np.newaxis] * directions
    return forces
