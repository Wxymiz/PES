from ..base_simulation_object import SimulationObject
import pygame

# Settings
PATH_SIZE = 10
PATH_COLOR = (200, 200, 200)

class Path(SimulationObject):
    def __init__(self, x, y, x2, y2, name, sprite):# w sumie to sprite nie potrzebny an razie moze potem bedzie ale na razie nie wanze to jest XD
        super().__init__(x, y, sprite)
        self.draw_priority = 1
        self.name = name
        self.x2 = x2
        self.y2 = y2
    
    def draw(self, screen):
        pygame.draw.line(screen, PATH_COLOR, (self.x, self.y), (self.x2, self.y2), PATH_SIZE)