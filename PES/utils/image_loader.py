import pygame

class ImageLoader:
    @staticmethod
    def load_image(image_name, size=None):
        image_path = "PES\\graphics\\"+image_name+".png"
        surface = pygame.image.load(image_path).convert_alpha()
        if size is not None:
            surface = pygame.transform.smoothscale(surface, size)
        return surface

