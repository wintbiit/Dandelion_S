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

        self.land = np.zeros((width, height), dtype=np.int32)
        self.land[0, 0] = 1
        self.fig, self.ax = plt.subplots()
        self.img = self.ax.imshow(self.land, cmap='Greens', interpolation='nearest')
        self.img.set_clim(vmin=env.config['VISUAL_VMIN'], vmax=env.config['VISUAL_VMAX'])
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def update(self, frame: int):
        sys.stdout.write(f'\rFrame {frame + 1}/{self.frames}')
        sys.stdout.flush()
        if frame == self.frames - 1:
            print()
            self.ani.event_source.stop()
        if self.paused:
            return self.img,
        # 场地上每一块的植物，每一块上有多个植物的遍历
        for x in range(self.width):
            for y in range(self.height):
                for seed in range(self.land[x, y]):
                    plant_height = self.env.generate_plant_height()
                    dx, dy = self.env.generate_distance_int(plant_height)
                    if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                        continue
                    self.land[x + dx, y + dy] += 1

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
