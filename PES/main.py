import json
import pygame, random
pygame.init() # Inicjalizacja procesow pygame

import simulation
import window
import objects
from utils import ImageLoader,SpritesExamplesCreator as SpEC

def main():
    # Inicjalizacja okna symulacji
    okienko = window.Window(width=1920, height=1080, title="PES")
    # Zaladowanie obrazu tla
    background = ImageLoader.load_image('background').convert()
    # Ustawienie obrazu tla na tlo okienka
    okienko.set_background(background)
    # Tworzenie obiektów do symulacji
    students = [
        objects.students.Freshman(359,359, ImageLoader.load_image(image_name="freshman",size=(40,40)), "Mariusz", next_course=''),
        objects.students.Freshman(359,359, ImageLoader.load_image(image_name="freshman",size=(40,40)), "Ziemowit", next_course=''),
        objects.students.Overachiever(359,359, ImageLoader.load_image(image_name="overachiever",size=(40,40)), "Karol", next_course=''),
        objects.students.Droppeddown(359,359, ImageLoader.load_image(image_name="droppeddown",size=(40,40)), "Boguslaw", next_course=''),
        objects.students.Slacker(359,359, ImageLoader.load_image(image_name="slacker",size=(40,40)), "Marek", next_course=''),
        objects.students.Slacker(359,359, ImageLoader.load_image(image_name="slacker",size=(40,40)), "Maciek", next_course='')
    ]
    buildings = [
        objects.Building(x=360, y=198, sprite=SpEC.get_surface(color='green', text='A7'), name="A7"),
        objects.Building(x=583, y=602, sprite=SpEC.get_surface(color='green', text='A2'), name="A2"),
        objects.Building(x=781, y=601, sprite=SpEC.get_surface(color='green', text='A4'), name="A4"),
        objects.Building(x=537, y=268, sprite=SpEC.get_surface(color='green', text='A5'), name="A5"),
        objects.Building(x=541, y=461, sprite=SpEC.get_surface(color='green', text='A3'), name="A3"),
        objects.Building(x=736, y=357, sprite=SpEC.get_surface(color='green', text='A1'), name="A1"),

        objects.Building(x=322, y=613, sprite=SpEC.get_surface(color='green', text='B2'), name="B2"),
        objects.Building(x=784, y=673, sprite=SpEC.get_surface(color='green', text='B5'), name="B5"),

        objects.Building(x=69, y=89, sprite=SpEC.get_surface(color='green', text='C1'), name="C1"),
        objects.Building(x=68, y=214, sprite=SpEC.get_surface(color='green', text='C2'), name="C2"),
        objects.Building(x=69, y=318, sprite=SpEC.get_surface(color='green', text='C16'), name="C16"),
        objects.Building(x=295, y=308, sprite=SpEC.get_surface(color='green', text='C6'), name="C6"),
        objects.Building(x=390, y=697, sprite=SpEC.get_surface(color='green', text='C5'), name="C5"),
        objects.Building(x=579, y=820, sprite=SpEC.get_surface(color='green', text='C15'), name="C15"),
        objects.Building(x=680, y=600, sprite=SpEC.get_surface(color='green', text='C21'), name="C21"),
        objects.Building(x=701, y=133, sprite=SpEC.get_surface(color='green', text='C8'), name="C8"),

        objects.Building(x=198, y=458, sprite=SpEC.get_surface(color='green', text='D8'), name="D8"),
        objects.Building(x=296, y=198, sprite=SpEC.get_surface(color='green', text='D3'), name="D3"),
        objects.Building(x=537, y=135, sprite=SpEC.get_surface(color='green', text='D1'), name="D1"),
        objects.Building(x=347, y=506, sprite=SpEC.get_surface(color='green', text='D4'), name="D4"),

        objects.Building(x=69, y=467, sprite=SpEC.get_surface(color='green', text='E3'), name="E3"),
        objects.Building(x=296, y=83, sprite=SpEC.get_surface(color='green', text='E7'), name="E7"),
        objects.Building(x=359, y=359, sprite=SpEC.get_surface(color='green', text='E1'), name="E1"),
        objects.Building(x=481, y=821, sprite=SpEC.get_surface(color='green', text='E24'), name="E24"),   
    ]
    pubs = [
        objects.Building(x=62, y=666, sprite=SpEC.get_surface(color='green', text='PUB2'), name="PUB2"),
        objects.Building(x=61, y=754, sprite=SpEC.get_surface(color='green', text='PUB3'), name="PUB3"),
        objects.Building(x=347, y=424, sprite=SpEC.get_surface(color='green', text='PUB1'), name="PUB1"),
        objects.Building(x=890, y=837, sprite=SpEC.get_surface(color='green', text='PUB5'), name="PUB5"),
        objects.Building(x=1050, y=283, sprite=SpEC.get_surface(color='green', text='PUB4'), name="PUB4"),
        objects.Building(x=1053, y=411, sprite=SpEC.get_surface(color='green', text='PUB6'), name="PUB6")
    ]
    path_objects = [] #objects.paths.Path(0,0,200,200,SpEC.get_surface(color='green'))
    with open('mapa.json', 'r') as plik:
        dane = json.load(plik)
    R_slownik = {k: tuple(v) for k, v in dane['waypoints'].items()}
    R_lista_polaczen = [tuple(x) for x in dane['connections']]
    R_wspolrzedne_polaczen = [
        (x1, y1, x2, y2)
        for (p1, p2) in R_lista_polaczen
        for (x1, y1), (x2, y2) in [(R_slownik[p1], R_slownik[p2])]
    ]
    path_objects = []
    for i,droga in enumerate(R_wspolrzedne_polaczen):
        path_objects.append(objects.paths.Path(droga[0],droga[1],droga[2],droga[3],f"path_{i}",SpEC.get_surface(color='green')))

    # Inicjalizacja logiki symulacji
    simulation_logic = simulation.Logic()

    # Dodanie obiektow do symulacji
    for path in path_objects:
        simulation_logic.add_element("paths",path)
    for building in buildings:
        simulation_logic.add_element("buildings",building)
    for pub in pubs:
        simulation_logic.add_element("pubs",pub)
    for student in students:
        simulation_logic.add_element("students",student)
    # for path_object in path_objects:
    #     simulation_logic.add_element(path_object)

    # dousuniecia
    simulation_logic.map.wczytaj_z_pliku("mapa.json")
    # simulation_logic.elements['students']['Asia'].set_path(simulation_logic.map.find_path("C1","A1"))

    while True:
        okienko.handle_events() # Obsługuje zdarzenia (np. nacisniecia myszki)
        simulation_logic.update()  # Aktualizuje logikę symulacji
        okienko.draw(simulation_logic.elements) # Rysuje obiekty na ekranie

        # print(simulation_logic.elements['students']['Ola'].path)
        # print(simulation_logic.time_to_next_course)

if __name__ == "__main__":
    main()