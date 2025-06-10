from .map import Map
from objects.dead import DeadStudent
import math, random

class Logic:
    def __init__(self):
        # Wszystkie elementy w podziale na kategorie obiektow
        self.elements = {
            "students": {},
            "deads": {},
            "buildings": {},
            'pubs': {},
            "paths": {}
        }  # Słownik wszystkich elementów w grze {nazwa: obiekt}

        # Inicjalizowanie mapy sciezki dla studentow
        self.map = Map()

        # Zmienne swiata
        self.max_time_to_next_course = 5000
        self.time_to_next_course = self.max_time_to_next_course

    def add_element(self, objects_category: str, element):
        self.elements[objects_category][element.name] = element
    
    def get_elements(self):
        return self.elements
    
    def random_element_id(self,category_name: str):
        return random.choice(list(self.elements[category_name].keys()))

    def update(self):
        # Dzialanie symulacji - to blad ze tutaj jest to, ja wiem, ale nie chcialem juz robic simulation_manager ani nic takiego XD

        if self.time_to_next_course <= 0:
            self.time_to_next_course = self.max_time_to_next_course
        self.time_to_next_course -= 1
        # Wyznaczanie celu studentom
        for id, student in self.elements['students'].items():
            if not student.next_course:
                next_course = self.random_element_id('buildings')
                student.set_path(self.map.find_path(self.nearest_building_from_position(student.x,student.y),next_course))
                student.next_course = next_course
            if self.time_to_next_course <= 0:
                if not self.distance_between_objects('buildings',student.next_course,'students',student.name) < 50:
                    student.ects -= 5
                    if student.ects <= 0:
                        student.is_dead = True
                student.next_course = ''
            student.alkohol -= 1
        # Usuwanie studentow gdy odpadli
        for klucz in list(self.elements['students'].keys()):
            if self.elements['students'][klucz].is_dead:
                self.elements['deads']['deadstudent_'+self.elements['students'][klucz].name] = DeadStudent(self.elements['students'][klucz].x,self.elements['students'][klucz].y,'deadstudent_'+self.elements['students'][klucz].name,self.elements['students'][klucz].width,self.elements['students'][klucz].height)
                del self.elements['students'][klucz]

        #########################################################
        # Zaktualizowanie stanu gry (np. ruch postaci)
        for group in self.elements.values():
            for element in group.values():
                element.update()
    
    def distance_between_objects(self, category1_name, obj1_id, category2_name, obj2_id):
        p1 = self.elements[category1_name][obj1_id]
        p2 = self.elements[category2_name][obj2_id]
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        return math.sqrt(dx*dx + dy*dy)
    
    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def nearest_building_from_position(self,x,y):
        buildings = self.elements.get('buildings', {})
        if not buildings:
            return None, float('inf')

        min_dist = float('inf')
        nearest_id = None

        for obj_id, obj in buildings.items():
            dist = self.distance(x, y, obj.x, obj.y)
            if dist < min_dist:
                min_dist = dist
                nearest_id = obj_id

        return nearest_id
