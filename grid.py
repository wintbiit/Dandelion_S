from mesa import Agent


class Grid(Agent):
    """土地方格Agent"""
    def __init__(self, id, paradise):
        super().__init__(id, paradise)
        self.plants = []

    def step(self):
        pass

    def add_plant(self, plant):
        self.plants.append(plant)
        self.model.schedule.add(plant)

    def plant_count(self):
        return len(self.plants)

    def is_empty(self):
        return len(self.plants) == 0

    def mature_plant_count(self):
        return sum([1 for plant in self.plants if plant.is_mature()])