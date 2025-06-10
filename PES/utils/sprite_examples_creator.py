import pygame

libary_of_colors = {
    'white' : (255, 255, 255),
    'red' : (255, 0, 0),
    'black' : (0, 0, 0),
    'green' : (0, 255, 0),
    'blue' : (0, 0, 255)
}

class SpritesExamplesCreator:
    def get_surface(color='white',width=50,height=50,text=''):
        surface = pygame.Surface((width, height)) # Tworzy powierzchnię o wybranej wielkosci (piksele x piksele)
        surface.fill(libary_of_colors[color]) # Wypełnia sprita na wybrany kolor

        if text:
            pygame.font.init()  # Inicjalizacja fontów (na wszelki wypadek)
            font = pygame.font.SysFont(None, 24)  # Domyślna czcionka, rozmiar 24
            text_surf = font.render(text, True, libary_of_colors['black'])  # Czarny tekst
            text_rect = text_surf.get_rect(center=(width // 2, height // 2))
            surface.blit(text_surf, text_rect)  # Rysuje tekst na środku

        return surface