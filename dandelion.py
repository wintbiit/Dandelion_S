import numpy as np
from mesa import Agent


class Dandelion(Agent):
    """蒲公英Agent"""
    def __init__(self, id, paradise):
        super().__init__(id, paradise)
        self.lifespan = paradise.env.generate_lifespan_int()
        self.height = paradise.env.generate_plant_height()
        print("Dandelion {} with lifespan {} and height {}".format(id, self.lifespan, self.height))

    def step(self):
        self.lifespan -= 1
        if not self.is_mature():
            return

        seed_count = 2000 // np.abs(self.lifespan)
        # 生成种子
        for _ in range(seed_count):
            dx, dy = self.model.env.generate_distance_int(self.height)
            x, y = self.pos
            x, y = x + dx, y + dy
            if not self.model.grid.is_cell_empty((x, y)) or not self.model.is_in_grid((x, y)):
                continue
            neighbors = self.model.grid.get_neighbors((x, y), False, radius=self.model.env.neighbor_scan_radius)
            # 如果周围蒲公英数量超过阈值，则不生成种子
            if len(neighbors) > self.model.env.neighbor_threshold:
                continue
            self.model.spawn_dandelion(x, y)

    def is_mature(self):
        return self.lifespan < 0
