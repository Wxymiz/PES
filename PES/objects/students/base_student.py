from ..base_simulation_object import SimulationObject
import pygame, math

# GRAPHICS SETTINGS
# Size
MAX_BAR_WIDTH = 50
BAR_HEIGHT = 10
# Distance
ABOVE_BAR_DISTANCE_ALKOHOL = 20
ABOVE_BAR_DISTANCE_ECTS = 30
ABOVE_NAME_DISTANCE = -30
# Colors
COLOR_BAR_BACK = (100, 100, 100)
COLOR_BAR_ALKOHOL = (240, 210, 60)
COLOR_BAR_ECTS = (240, 50, 33)
COLOR_NAME = (255, 255, 255)
# Fonts
FONT_SIZE = 30
FONT_NAME = pygame.font.SysFont(None, FONT_SIZE)

class BaseStudent(SimulationObject):
    def __init__(self, x, y, sprite, name, speed, max_ects, alkohol, max_alkohol, next_course, path=None):
        super().__init__(x, y, sprite)
        self.draw_priority = 3
        self.name = name
        self.speed = speed
        self.ects = max_ects
        self.max_ects = max_ects
        self.alkohol = alkohol
        self.max_alkohol = max_alkohol
        self.next_course = next_course
        self.is_dead = False

        # Pathfinding initialization
        self.path = []  # lista punktów (x, y)
        self.path_index = 0

        # Sprite initialization
        self.name_sprite = FONT_NAME.render(self.name, True, COLOR_NAME)
        self.name_sprite_width,self.name_sprite_height = self.name_sprite.get_size()
        self.sprite_angle = 0
    
    def update(self):
        if self.path and self.path_index < len(self.path):
            target_x, target_y = self.path[self.path_index]
            dx = target_x - self.x
            dy = target_y - self.y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist < self.speed:
                self.x, self.y = target_x, target_y
                self.path_index += 1
            else:
                self.x += self.speed * dx / dist
                self.y += self.speed * dy / dist
            
            # Oblicz kąt w radianach i konwertuj na stopnie
            self.sprite_angle = math.degrees(math.atan2(-dy, dx))  # minus dy bo pygame y rośnie w dół

    def draw(self, screen):
        # super().draw(screen) jednak tego nie uzywamy XD
        # Obróć sprite o self.angle stopni
        rotated_sprite = pygame.transform.rotate(self.sprite, self.sprite_angle)
        rect = rotated_sprite.get_rect(center=(self.x, self.y))
        screen.blit(rotated_sprite, (self.x - self.width // 2, self.y - self.height // 2))
        # PASKI STANU
        # Alkohol
        pygame.draw.rect(screen, (100, 100, 100), (self.x - MAX_BAR_WIDTH // 2, self.y - ABOVE_BAR_DISTANCE_ALKOHOL, MAX_BAR_WIDTH, BAR_HEIGHT))
        pygame.draw.rect(screen, COLOR_BAR_ALKOHOL, (self.x - MAX_BAR_WIDTH // 2, self.y - ABOVE_BAR_DISTANCE_ALKOHOL, int(MAX_BAR_WIDTH * (self.alkohol / self.max_alkohol)), BAR_HEIGHT))
        # Ects
        pygame.draw.rect(screen, (100, 100, 100), (self.x - MAX_BAR_WIDTH // 2, self.y - ABOVE_BAR_DISTANCE_ECTS, MAX_BAR_WIDTH, BAR_HEIGHT))
        pygame.draw.rect(screen, COLOR_BAR_ECTS, (self.x - MAX_BAR_WIDTH // 2, self.y - ABOVE_BAR_DISTANCE_ECTS, int(MAX_BAR_WIDTH * (self.ects / self.max_ects)), BAR_HEIGHT))

        # Napis
        screen.blit(self.name_sprite, (self.x - self.name_sprite_width // 2, self.y - self.name_sprite_height // 2 - ABOVE_NAME_DISTANCE))
    
    def set_path(self, path):
        self.path = path
        self.path_index = 0


