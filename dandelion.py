import numpy as np
from mesa import Agent


class Dandelion(Agent):
    """蒲公英Agent"""

    def __init__(self, id, paradise, lifespan=None, height=None, distance=None):
        super().__init__(id, paradise)
        self.lifespan = lifespan if lifespan is not None else paradise.env.generate_lifespan_int()
        self.height = height if height is not None else paradise.env.generate_plant_height()
        self.distance = distance

        print("Dandelion {} with lifespan {} and height {}".format(id, self.lifespan, self.height))

    def step(self):
        self.lifespan -= 1
        if not self.is_mature():
            return

        seed_count = 20000 // np.abs(self.lifespan)

        claimed = 0
        out_of_bounds = 0
        occupied = 0
        out_of_resources = 0
        # 生成种子
        for _ in range(seed_count):
            dx, dy, distance = self.model.env.generate_distance_int(self.height)
            x, y = self.pos
            x, y = x + dx, y + dy
            if not self.model.is_in_grid((x, y)):  # 如果该位置不在网格内，则不生成种子
                out_of_bounds += 1
                continue
            if not self.model.grid.is_cell_empty((x, y)):  # 如果该位置已经有Agent，则不生成种子
                occupied += 1
                continue
            neighbors = self.model.grid.get_neighbors((x, y), False, radius=self.model.env.neighbor_scan_radius)
            if len(neighbors) > self.model.env.neighbor_threshold:  # 如果周围蒲公英数量超过阈值，则不生成种子
                out_of_resources += 1
                continue
            self.model.spawn_dandelion(x, y, distance=distance)
            claimed += 1

        print(
            "Dandelion {} with lifespan {} and height {} spreads {}/{} seeds, {} out of bounds, {} occupied, "
            "{} out of resources"
            .format(self.unique_id, self.lifespan,
                    self.height, claimed,
                    seed_count, out_of_bounds, occupied, out_of_resources))

    def is_mature(self):
        return self.lifespan < 0
