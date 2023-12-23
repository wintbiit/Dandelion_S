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
    'PLANT_LIFESPAN_MIN': int(os.getenv('PLANT_LIFESPAN_MIN')),
    'PLANT_LIFESPAN_MAX': int(os.getenv('PLANT_LIFESPAN_MAX')),
    'TEMPERATURE_MIN': int(os.getenv('TEMPERATURE_MIN')),
    'TEMPERATURE_MAX': int(os.getenv('TEMPERATURE_MAX')),
    'NEIGHBOR_SCAN_RADIUS': int(os.getenv('NEIGHBOR_SCAN_RADIUS')),
    'NEIGHBOR_THRESHOLD': int(os.getenv('NEIGHBOR_THRESHOLD')),
}


def generate_distance(plant_height, horizontal_wind, vertical_wind, subside_speed, subside_height):
    """风传播距离"""
    horizontal_wind_speed = np.sqrt(horizontal_wind[0] ** 2 + horizontal_wind[1] ** 2)

    distance = 0.4 * horizontal_wind_speed / np.log((subside_height - 0.63 * plant_height) / 0.13 * plant_height) \
               * ((subside_height - 0.63 * plant_height) * np.log(
        (subside_height - 0.63 * plant_height) / (np.e * 0.13 * plant_height)) + 0.13 * plant_height) \
               / 0.4 / (subside_speed - vertical_wind)

    if np.isnan(distance):
        distance = 0

    # 在 horizontal_wind 的方向上，大小为 distance 的向量
    return (horizontal_wind[0] / horizontal_wind_speed * distance,
            horizontal_wind[1] / horizontal_wind_speed * distance)


def generate_distance_int(plant_height, horizontal_wind, vertical_wind, subside_speed, subside_height):
    dx, dy = generate_distance(plant_height, horizontal_wind, vertical_wind, subside_speed, subside_height)

    return math.floor(dx), math.floor(dy)


class EnvironmentGenerator:
    def __init__(self, config=None):
        if config is None:
            config = config_env
        self.config = config
        self.current_wind = None
        self.current_vertical_wind = None
        self.current_subside_speed = None
        self.current_subside_height = None
        self.current_temperature = None
        self.step()

        self.neighbor_scan_radius = config['NEIGHBOR_SCAN_RADIUS']
        self.neighbor_threshold = config['NEIGHBOR_THRESHOLD']

    def step(self):
        self.current_wind = self.generate_wind_horizontal()
        self.current_vertical_wind = self.generate_wind_vertical()
        self.current_subside_speed = self.generate_subside_speed()
        self.current_subside_height = self.generate_subside_height()
        self.current_temperature = self.generate_temperature()

    def generate_distance(self, plant_height):
        return generate_distance(plant_height, self.current_wind, self.current_vertical_wind, self.current_subside_speed,
                                 self.current_subside_height)

    def generate_lifespan(self):
        """随机产生植物寿命"""
        return 10 * np.exp(0.001109 * (self.current_temperature - 55) ** 2) + 75

    def generate_distance_int(self, plant_height):
        return generate_distance_int(plant_height, self.current_wind, self.current_vertical_wind,
                                     self.current_subside_speed, self.current_subside_height)

    def generate_lifespan_int(self) -> int:
        """随机产生植物寿命"""
        return math.floor(self.generate_lifespan())

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

    def generate_temperature(self):
        """随机产生温度"""
        return np.random.randint(self.config['TEMPERATURE_MIN'], self.config['TEMPERATURE_MAX'])


