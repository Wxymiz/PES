from ..base_simulation_object import SimulationObject
from utils import ImageLoader

class DeadStudent(SimulationObject):
    def __init__(self, x, y, name, width, height):
        super().__init__(x, y, sprite=ImageLoader.load_image("dead",(width,height)))
        self.draw_priority = 2
        self.name = name

