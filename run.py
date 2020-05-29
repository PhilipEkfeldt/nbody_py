from classes import *
from physics import *

planet = Planet(
    position=np.array([0.0, 0.0, 0.0]),
    velocity=np.array([0.0, 0.0, 0.0]),
    mass=333000.0,
    radius=2e3,
    color="green",
)

planet2 = Planet(
    position=np.array([5.0, 0.0, 0.0]),
    velocity=np.array([0, 2, 0.0]) * 1e-7,
    mass=333000.0,
    radius=1e3,
    color="green",
)

planet3 = Planet(
    position=np.array([1.0, 0.0, 0.0]),
    velocity=np.array([0.0, 3.0, 0.0]) * 1e-7,
    mass=333000.0 / 2,
    radius=2e3,
    color="green",
)

s = System([planet, planet2, planet3])


s.run(timestep=1e4, speed=1e6, iterations=100000)
