import numpy as np
from math import *
from tkinter import *
from classes import *
import time


def disp(obstacle):
    posx, posy = 55, 60
    window = Tk()
    canvas = Canvas(window, width = 600, height = 600, background='white')
    for i in range(obstacle.size):
        line = obstacle.getline(i)
        canvas.create_line(line.start[0], line.start[1], line.end[0], line.end[1])
    vehicle = canvas.create_polygon(50, 50, 60, 50, 55, 60)
    canvas.pack()
    dy = 2
    while posy < 580:
        time.sleep(1.0/24.0)
        posy = posy + dy
        canvas.move(vehicle, 0, dy)
        canvas.update()
    window.mainloop()
