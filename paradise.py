import sys
import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from env_generator import EnvironmentGenerator


class Paradise:
    """Dandelion Spread Simulation Environment"""

    def __init__(self, width: int, height: int, env: EnvironmentGenerator):
        self.interval: int = 0
        self.frames: int = 0
        self.paused = False
        self.ani: FuncAnimation = None

        self.width = width
        self.height = height
        self.env = env

        self.land = np.zeros((width, height), dtype=np.float32)
        self.land[0, 0] = 0.1
        self.fig, self.ax = plt.subplots()
        self.img = self.ax.imshow(self.land, cmap='Greens', interpolation='nearest')
        self.img.set_clim(vmin=0, vmax=3)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def update(self, frame: int):
        sys.stdout.write(f'\rFrame {frame + 1}/{self.frames}')
        sys.stdout.flush()
        if frame == self.frames - 1:
            print()
            self.ani.event_source.stop()
        new_seeds = np.argwhere(self.land > 0)
        for seed in new_seeds:
            x, y = seed
            height = self.env.generate_plant_height()
            dx, dy = self.env.generate_distance_int(height)
            if 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                self.land[x + dx, y + dy] += 0.1
        self.img.set_array(self.land)
        return self.img,

    def show(self, frames: int, interval: int):
        self.frames = frames
        self.interval = interval
        self.ani = FuncAnimation(self.fig, self.update, frames=frames, interval=interval, blit=True)
        plt.title('Dandelion Spread Simulation')
        plt.colorbar(self.img, label='Dandelion presence')
        plt.xlabel('Width')
        plt.ylabel('Height')
        plt.show(block=False)
        print('Simulation finished')
        plt.waitforbuttonpress()
        plt.close()

    def on_key_press(self, event):
        if event.key == ' ':  # Pause
            self.paused = not self.paused
            if self.paused:
                self.ani.pause()
            else:
                self.ani.resume()
        elif event.key == 'enter':  # Save
            plt.savefig("dandelion_spread-" + time.strftime("%Y%m%d-%H%M%S") + ".png")
        elif event.key == 'escape':
            plt.close()
        elif event.key == 'a':
            plt.close()
            print('Saving GIF...')
            self.ani.save('dandelion_spread.gif', writer='pillow', fps=30)
            print('GIF saved')
        elif event.key == 'r':
            plt.close()
            self.show(self.frames, self.interval)
