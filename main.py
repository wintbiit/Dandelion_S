import argparse
import time

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from env_generator import EnvironmentGenerator
from paradise import Paradise

ani: FuncAnimation
paused = False
paradise: Paradise
args: argparse.Namespace


def main():
    global args
    global paradise
    global ani

    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=100)
    parser.add_argument('--height', type=int, default=100)
    parser.add_argument('--interval', type=int, default=500)
    parser.add_argument('--frames', type=int, default=100)

    args = parser.parse_args()

    config = {
        'HORIZ_WIND_MIN': -3,
        'HORIZ_WIND_MAX': 3,
        'VERT_WIND_MIN': -0.1,
        'VERT_WIND_MAX': 0.1,
        'SUBSIDE_HEIGHT_MIN': 0.1,
        'SUBSIDE_HEIGHT_MAX': 0.5,
        'SUBSIDE_SPEED_MIN': 0.1,
        'SUBSIDE_SPEED_MAX': 0.5,
        'PLANT_HEIGHT_MIN': 0.1,
        'PLANT_HEIGHT_MAX': 0.5
    }

    env = EnvironmentGenerator(config)

    paradise = Paradise(args.width, args.height, env)
    paradise.fig.canvas.mpl_connect('key_press_event', on_key_press)

    ani = FuncAnimation(paradise.fig, paradise.update, frames=args.frames, interval=args.interval, blit=True)

    plt.title('Dandelion Spread Simulation')
    plt.colorbar(paradise.img, label='Dandelion presence')
    plt.xlabel('Width')
    plt.ylabel('Height')
    plt.show()

    ani.event_source.stop()

    print('Simulation finished')
    ani.save('dandelion_spread.gif', writer='pillow', fps=30)

    # wait for the user to close the window
    plt.waitforbuttonpress()


def on_key_press(event):
    global ani
    global paused
    if event.key == ' ':  # Pause
        paused = not paused
        if paused:
            ani.pause()
        else:
            ani.resume()
    elif event.key == 'enter':  # Save
        plt.savefig("dandelion_spread-" + time.strftime("%Y%m%d-%H%M%S") + ".png")
    elif event.key == 'escape':
        plt.close()
    elif event.key == 'a':
        ani.pause()
        ani.save('dandelion_spread.gif', writer='pillow', fps=30)
        ani.resume()
    elif event.key == 'r':
        ani.event_source.stop()
        ani = FuncAnimation(paradise.fig, paradise.update, frames=args.frames, interval=args.interval, blit=True)
        ani.event_source.start()


if __name__ == '__main__':
    main()
