from .base_student import BaseStudent

class Slacker(BaseStudent):
    def __init__(self, x, y, sprite, name, next_course, path=None):
        super().__init__(x=x, y=y, sprite=sprite, name=name, speed=0.1, max_ects=15, alkohol=30000, max_alkohol=60000, next_course=next_course, path=path)