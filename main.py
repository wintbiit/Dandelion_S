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

    env = EnvironmentGenerator()

    paradise = Paradise(args.width, args.height, env)
    paradise.show(args.frames, args.interval)


if __name__ == '__main__':
    main()
