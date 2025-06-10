from .base_simulation_object import SimulationObject

class Building(SimulationObject):
    def __init__(self, x, y, sprite, name):
        super().__init__(x, y, sprite)
        self.draw_priority = 2
        self.name = name