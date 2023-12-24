from matplotlib import pyplot as plt
from mesa import Model, DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from dandelion import Dandelion
from env_generator import EnvironmentGenerator


class Paradise(Model):
    """生长环境Model"""
    def __init__(self, width, height):
        super().__init__()
        self.env = EnvironmentGenerator()
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters={
                "Mature": lambda m: m.plant_count(),
                "Temperature": lambda m: m.env.current_temperature,
            },
            agent_reporters={
                "AgentID": lambda a: a.unique_id,
                "Lifespan": lambda a: a.lifespan,
            }
        )

        # 左上角生成蒲公英
        self.spawn_dandelion(0, 0, 0)

    def step(self):
        self.env.step()  # 更新环境
        self.schedule.step()  # 更新Agent
        self.datacollector.collect(self)

    def plant_count(self):
        """成熟的蒲公英数量"""
        return sum([1 for agent in self.schedule.agents if agent.is_mature()])

    def is_in_grid(self, pos):
        x, y = pos
        return 0 <= x < self.grid.width and 0 <= y < self.grid.height

    def spawn_dandelion(self, x, y, lifespan=None, height=None):
        dandelion = Dandelion(self.next_id(), self, lifespan, height)
        self.grid.place_agent(dandelion, (x, y))
        self.schedule.add(dandelion)

    def visualize(self):
        plt.figure(figsize=(8, 6))
        colors = ['yellow', 'blue']

        for cell_content, (x, y) in self.grid.coord_iter():
            if cell_content:
                plt.scatter(x, y, color='green', s=50 * len(cell_content))

        plt.title("Dandelion Spread Simulation")
        plt.xlabel("Width")
        plt.ylabel("Height")
        plt.show()

        self.datacollector.get_agent_vars_dataframe().groupby('AgentID').plot()


