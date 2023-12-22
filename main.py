import argparse

from env_generator import EnvironmentGenerator
from paradise import Paradise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=100)
    parser.add_argument('--height', type=int, default=100)
    parser.add_argument('--interval', type=int, default=500)
    parser.add_argument('--frames', type=int, default=100)

    args = parser.parse_args()      # 从命令行读取参数

    env = EnvironmentGenerator()    # 生成环境

    paradise = Paradise(args.width, args.height, env)
    paradise.show(args.frames, args.interval)       # 显示


if __name__ == '__main__':
    main()
