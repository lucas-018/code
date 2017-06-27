import numpy as np
from math import *

class Line:
    def __init__(self, start, end):
        self._start = start
        self._end = end
    @property
    def start(self):
        return self._start
    @property
    def end(self):
        return self._end

class Obstacle:
    def __init__(self, input_tab=None):
        if input_tab is None:
            self._tab = []
        else:
            self._tab = input_tab
    def getline(self, ind):
        return self._tab[ind]
    def addline(self, input_line):
        self._tab += [input_line]
    @property
    def size(self):
        return len(self._tab)

class Drone:
    def __init__(self, force_motors, coeff_air, mass, pos, speed, direction):
        self._force = force_motors
        self._coeff = coeff_air
        self._mass = mass
        self._speed = speed
        self._dir = direction
        self._pos = pos
    def compute_acceleration(self):
        self._acc = self._force*self._dir - self._coeff*(self._speed*self._speed)
    def compute_speed(self, dt):
        self._speed = self._speed + self.acc*dt
    def compute_position(self, dt):
        self._pos = self._pos + self._speed*dt
    def update(self, dt):
        self.compute_acceleration(dt)
        self.compute_speed(dt)
        self.compute_position(dt)
    def change_dir(self, dis):
        if dis == -1:







LINE_1 = Line(np.array([20, 20]), np.array([580, 20]))
LINE_2 = Line(np.array([580, 20]), np.array([580, 580]))
LINE_3 = Line(np.array([580, 580]), np.array([20, 580]))
LINE_4 = Line(np.array([20, 580]), np.array([20, 20]))
TAB= [LINE_1, LINE_2, LINE_3, LINE_4]

OBSTACLE = Obstacle(TAB)
