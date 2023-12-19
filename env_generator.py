import math
import os

import numpy as np
from dotenv import load_dotenv

load_dotenv()
config_env = {
    'HORIZ_WIND_MIN': float(os.getenv('HORIZ_WIND_MIN')),
    'HORIZ_WIND_MAX': float(os.getenv('HORIZ_WIND_MAX')),
    'VERT_WIND_MIN': float(os.getenv('VERT_WIND_MIN')),
    'VERT_WIND_MAX': float(os.getenv('VERT_WIND_MAX')),
    'SUBSIDE_HEIGHT_MIN': float(os.getenv('SUBSIDE_HEIGHT_MIN')),
    'SUBSIDE_HEIGHT_MAX': float(os.getenv('SUBSIDE_HEIGHT_MAX')),
    'SUBSIDE_SPEED_MIN': float(os.getenv('SUBSIDE_SPEED_MIN')),
    'SUBSIDE_SPEED_MAX': float(os.getenv('SUBSIDE_SPEED_MAX')),
    'PLANT_HEIGHT_MIN': float(os.getenv('PLANT_HEIGHT_MIN')),
    'PLANT_HEIGHT_MAX': float(os.getenv('PLANT_HEIGHT_MAX')),
}


class EnvironmentGenerator:
    def __init__(self, config=None):
        if config is None:
            config = config_env
        self.config = config

    def generate_wind_horizontal(self):
        """随机水平风速"""
        return (np.random.uniform(self.config['HORIZ_WIND_MIN'], self.config['HORIZ_WIND_MAX']),
                np.random.uniform(self.config['HORIZ_WIND_MIN'], self.config['HORIZ_WIND_MAX']))

    def generate_wind_vertical(self):
        """随机垂直风速"""
        return np.random.uniform(self.config['VERT_WIND_MIN'], self.config['VERT_WIND_MAX'])

    def generate_subside_height(self):
        """随机沉降高度"""
        return np.random.uniform(self.config['SUBSIDE_HEIGHT_MIN'], self.config['SUBSIDE_HEIGHT_MAX'])

    def generate_subside_speed(self):
        """随机沉降速度"""
        return np.random.uniform(self.config['SUBSIDE_SPEED_MIN'], self.config['SUBSIDE_SPEED_MAX'])

    def generate_plant_height(self):
        """随机植物高度"""
        return np.random.uniform(self.config['PLANT_HEIGHT_MIN'], self.config['PLANT_HEIGHT_MAX'])

    def generate_distance(self, plant_height):
        """风传播距离"""
        horizontal_wind = self.generate_wind_horizontal()
        horizontal_wind_speed = np.sqrt(horizontal_wind[0] ** 2 + horizontal_wind[1] ** 2)
        vertical_wind_speed = self.generate_wind_vertical()
        subside_speed = self.generate_subside_speed()
        subside_height = self.generate_subside_height()

        distance = 0.4 * horizontal_wind_speed / np.log((subside_height - 0.63 * plant_height) / 0.13 * plant_height) \
                   * ((subside_height - 0.63 * plant_height) * np.log(
            (subside_height - 0.63 * plant_height) / (np.e * 0.13 * plant_height)) + 0.13 * plant_height) \
                   / 0.4 / (subside_speed - vertical_wind_speed)

        if np.isnan(distance):
            distance = 0

        # 在 horizontal_wind 的方向上，大小为 distance 的向量
        return (horizontal_wind[0] / horizontal_wind_speed * distance,
                horizontal_wind[1] / horizontal_wind_speed * distance)

    def generate_distance_int(self, plant_height: float) -> tuple:
        dx, dy = self.generate_distance(plant_height)

        return math.floor(dx), math.floor(dy)
