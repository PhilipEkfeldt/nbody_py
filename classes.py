from __future__ import annotations
import numpy as np
from typing import List, Type, Any
import nptyping as npt
from physics import gravity
from vpython import *
from astropy.constants import M_earth, M_sun, R_earth, R_sun, au
from astropy.units import second, kg
import time


class Planet:
    def __init__(
        self,
        position: npt.NDArray[(Any), float],
        velocity: npt.NDArray[(Any), float],
        mass: float,
        radius: float,
        color: str,
    ) -> None:
        if len(velocity) > 3 or len(velocity) < 2:
            raise ValueError("Velocity must be 2 or 3 dimensional")
        if len(position) > 3 or len(position) < 2:
            raise ValueError("Position must be 2 or 3 dimensional")
        if len(position) != len(velocity):
            raise ValueError("Position and velocity must be the same dimension")

        self._dimensions = len(position)
        self._force = 0
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.radius = radius
        self._color = color
        self.draw_obj = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        if len(new_position) != self._dimensions:
            raise ValueError(f"Position must be {self._dimensions} dimensions")
        elif not all(isinstance(d, float) for d in new_position):
            raise ValueError("All position coordinates must be floats")
        self._position = new_position * au

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, new_velocity):
        if len(new_velocity) != self._dimensions:
            raise ValueError(f"Velocity must be {self._dimensions} dimensions")
        elif not all(isinstance(d, float) for d in new_velocity):
            raise ValueError("All velocity coordinates must be floats")
        self._velocity = new_velocity * au / second

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, new_mass):
        if new_mass <= 0:
            raise ValueError("Mass must be larger than 0")
        self._mass = new_mass * M_earth

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, new_radius):
        if new_radius <= 0:
            raise ValueError("Radius must be larger than 0")
        self._radius = new_radius * R_earth

    @property
    def color(self):
        return self._color

    def update_position(self, timestep):
        self._position = self._position + self._velocity * timestep * second
        if self.draw_obj != None:
            p = tuple((self._position / au).value)
            # print(p)
            self.draw_obj.pos = vector(p[0], p[1], p[2])

    def update_velocity(self, timestep, force):
        self._force = force
        self._velocity = self._velocity + self._force / self._mass * timestep * second

    def __str__(self):
        return (
            str(self.__class__)
            + "\n"
            + "\n".join(
                (
                    str(item) + " = " + str(self.__dict__[item])
                    for item in sorted(self.__dict__)
                )
            )
        )


class System:
    def __init__(self, objects: List[Planet]) -> None:
        self._objects = objects
        # ADD CHECK FOR 2D/3D, sanity check on input objects (Auto-derive?)

    @property
    def objects(self):
        return self._objects

    def update(self, timestep):
        positions = np.stack([planet.position for planet in self._objects], axis=0)
        masses = np.array([np.array(planet.mass) for planet in self._objects]) * kg
        forces = gravity(positions, masses)
        force_tot = np.sum(forces, axis=1)

        for i, planet in enumerate(self._objects):
            planet.update_position(timestep)
            planet.update_velocity(timestep, force_tot[i])

    def run(self, timestep: float, speed: int = 1, iterations: int = 100) -> System:
        r = speed / timestep
        for planet in self._objects:
            p = tuple((planet.position / au).value)
            print("Radius: ", planet.radius / au)
            print("Position: ", p)
            planet.draw_obj = sphere(
                pos=vector(p[0], p[1], p[2]),
                radius=planet.radius / au,
                color=color.yellow,
                make_trail=True,
                trail_type="points",
                interval=100,
                retain=50,
            )

        for i in range(iterations):
            rate(r)
            self.update(timestep)

        return self


p = Planet(
    position=np.array([2.0, 3.0]),
    velocity=np.array([2.0, 3.0]),
    mass=1.0,
    radius=1.0,
    color="green",
)

