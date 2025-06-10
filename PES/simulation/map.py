from collections import deque
import json

class Map:
    def __init__(self):
        self.punkty = {}          # nazwa → (x, y)
        self.polaczenia = set()   # zbiór krotek (nazwa1, nazwa2)

    def connect_waypoints(self, nazwa1, nazwa2):
        if nazwa1 in self.punkty and nazwa2 in self.punkty:
            klucz = tuple(sorted((nazwa1, nazwa2)))
            self.polaczenia.add(klucz)
        else:
            print(f"Nie można połączyć: '{nazwa1}' lub '{nazwa2}' nie istnieje w mapie.")
    
    def add_waypoint(self, obj):
        name = obj.name
        pos = (obj.x, obj.y)
        self.punkty[name] = pos


    def find_path(self, start, cel):
        if start not in self.punkty or cel not in self.punkty:
            return []

        visited = set()
        queue = deque([(start, [start])])

        while queue:
            current, path = queue.popleft()
            if current == cel:
                return [tuple(self.punkty[n]) for n in path]

            visited.add(current)
            for a, b in self.polaczenia:
                sąsiedni = []
                if a == current:
                    sąsiedni.append(b)
                elif b == current:
                    sąsiedni.append(a)

                for sąsiad in sąsiedni:
                    if sąsiad not in visited:
                        queue.append((sąsiad, path + [sąsiad]))
        return []

    def get_map(self):
        return {
            "punkty": self.punkty,
            "polaczenia": list(self.polaczenia)
        }
    
    def wczytaj_z_pliku(self, nazwa_pliku):
        try:
            with open(nazwa_pliku, 'r', encoding='utf-8') as plik:
                dane = json.load(plik)

            self.punkty = dane.get("waypoints", {})
            
            # Zamiana listy list na zbiór krotek
            self.polaczenia = set(tuple(pary) for pary in dane.get("connections", []))

        except FileNotFoundError:
            print(f"Błąd: Plik '{nazwa_pliku}' nie został znaleziony.")
        except json.JSONDecodeError:
            print(f"Błąd: Niepoprawny format JSON w pliku '{nazwa_pliku}'.")
