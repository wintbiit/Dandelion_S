import matplotlib.pyplot as plt
import numpy as np

from env_generator import EnvironmentGenerator


class Paradise:
    """Dandelion Spread Simulation Environment"""
    def __init__(self, width: int, height: int, env: EnvironmentGenerator):
        self.width = width
        self.height = height
        self.env = env
        self.land = np.zeros((width, height))
        self.land[0, 0] = 1
        self.fig, self.ax = plt.subplots()
        self.img = self.ax.imshow(self.land, cmap='Greens', interpolation='nearest')

    def update(self, frame: int):
        new_seeds = np.argwhere(self.land == 1)
        for seed in new_seeds:
            x, y = seed
            height = self.env.generate_plant_height()
            dx, dy = self.env.generate_distance_int(height)
            if 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                self.land[x + dx, y + dy] = 1
        self.img.set_array(self.land)
        return self.img,

