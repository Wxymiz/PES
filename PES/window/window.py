import pygame

class Window:
    def __init__(self, width=1200, height=800, title="My Window"):
        pygame.init()
        self.width = width
        self.height = height
        self.title = title
        self.fullscreen = False
        self.flags = 0  # Brak flag na start
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        # Funkcja ktora rysyje tlo (dwie opcje - fill or blit - czyli ablo kolorem, albo obrazem)
        self.clear_screen = self._clear_with_color

        # Tlo - opcjonalne
        self.background = None

    def handle_events(self):
        # Obsługuje zdarzenia takie jak naciśnięcia klawiszy, kliknięcia myszy itp.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
    
    def _clear_with_color(self):
        self.screen.fill((128, 128, 128)) # Wypełnia ekran wybranym kolorem RGB
    
    def _clear_with_image(self):
        self.screen.blit(self.background, (0, 0)) # Wypełnia ekran wybranym obrazem
    
    def set_background(self,sprite):
        self.background = sprite
        self.clear_screen = self._clear_with_image

    def draw(self, elements): # Elementy rysowane sa po self.draw_priority (tym wieksze, tym pozniej rysowane - tym bardziej na wierzchu sa)
        # Rysowanie wszystkich elementów (np. postaci, budynków) na ekranie
        self.clear_screen()

        list_of_elements = [char for group in elements.values() for char in group.values()]
        elements_sorted = sorted(list_of_elements, key=lambda e: getattr(e, "draw_priority", 100))

        for element in elements_sorted:
            element.draw(self.screen)
        pygame.display.flip()
    
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.flags = pygame.FULLSCREEN
        else:
            self.flags = 0
        self.screen = pygame.display.set_mode((self.width, self.height), self.flags)

