class SimulationObject:
    def __init__(self, x, y, sprite):
        self.draw_priority = 1
        self.x = x
        self.y = y
        self.sprite = sprite
        
        self.width, self.height = self.sprite.get_size()
    
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.sprite, (self.x - self.width // 2, self.y - self.height // 2))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())