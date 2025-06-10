import pygame
import sys
import math
import string
import json

def save_map(filename, waypoints, connections):
    # Struktura do zapisu
    data = {
        "waypoints": waypoints,
        "connections": connections
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Mapa zapisana do pliku {filename}")

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # lub SCREEN_WIDTH, SCREEN_HEIGHT
pygame.display.set_caption("Tworzenie mapy z waypointami")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

fullscreen = False

WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
RED = (255, 50, 50)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
LIGHT_GRAY = (200,200,200)

WAYPOINT_RADIUS = 8

MAP_WIDTH = 1000
MAP_HEIGHT = 1000

waypoints = {}
connections = []

def name_generator():
    from itertools import product
    chars = string.ascii_uppercase
    for size in range(1, 3):
        for letters in product(chars, repeat=size):
            yield ''.join(letters)

name_gen = name_generator()

camera_offset = [0, 0]
CAMERA_SPEED = 10  # Przesuwanie kamery o 10 pikseli

def get_nearest_waypoint(pos, radius=10):
    for name, coords in waypoints.items():
        wp_pos = (coords[0] + camera_offset[0], coords[1] + camera_offset[1])
        if math.hypot(pos[0] - wp_pos[0], pos[1] - wp_pos[1]) < radius:
            return name
    return None

def point_line_distance(p, a, b):
    # Odległość punktu p od odcinka ab
    px, py = p
    ax, ay = a
    bx, by = b
    # jeśli a==b, odległość to odległość do punktu a
    if ax == bx and ay == by:
        return math.hypot(px - ax, py - ay)
    # projekcja punktu p na prostą ab
    t = ((px - ax)*(bx - ax) + (py - ay)*(by - ay)) / ((bx - ax)**2 + (by - ay)**2)
    t = max(0, min(1, t))
    proj_x = ax + t*(bx - ax)
    proj_y = ay + t*(by - ay)
    return math.hypot(px - proj_x, py - proj_y)

running = True
selected = None

editing_name = False
editing_wp = None
input_text = ""

menu_active = False
menu_wp_selected = None

delete_connection_mode = False  # tryb usuwania połączeń

# Pozycja i wymiary menu (na dole ekranu)
MENU_X = 550
MENU_HEIGHT = 200
MENU_Y = 600 - MENU_HEIGHT - 10  # 10 px od dołu
MENU_WIDTH = 220

buttons = [
    {"label": "Usuń waypoint", "action": "delete_wp"},
    {"label": "Usuń połączenia (tryb)", "action": "delete_connections"},
    {"label": "Opcja 3 (pusta)", "action": None},
    {"label": "Opcja 4 (pusta)", "action": None},
]

def draw_button(surface, rect, text, active=True):
    color = DARK_GRAY if active else GRAY
    pygame.draw.rect(surface, color, rect)
    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)

while running:
    screen.fill(LIGHT_GRAY)

    # Rysowanie obramowania mapy z offsetem kamery
    map_rect = pygame.Rect(camera_offset[0], camera_offset[1], MAP_WIDTH, MAP_HEIGHT)
    pygame.draw.rect(screen, BLACK, map_rect, 2)  # 2 px grubość linii

    # Rysowanie połączeń z offsetem kamery
    for a, b in connections:
        start_pos = (waypoints[a][0] + camera_offset[0], waypoints[a][1] + camera_offset[1])
        end_pos = (waypoints[b][0] + camera_offset[0], waypoints[b][1] + camera_offset[1])
        pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)

    # Rysowanie waypointów z offsetem kamery
    for name, (x, y) in waypoints.items():
        pos = (x + camera_offset[0], y + camera_offset[1])
        pygame.draw.circle(screen, BLUE, pos, WAYPOINT_RADIUS)
        label = font.render(name, True, BLACK)
        screen.blit(label, (pos[0] + 10, pos[1] - 10))

    # Tekst edycji nazwy
    if editing_name and editing_wp:
        info_text = font.render(f"Podaj nazwę dla waypointa (Enter zatwierdza): {input_text}", True, RED)
        screen.blit(info_text, (10, 10))

    # Informacja o trybie usuwania połączeń
    if delete_connection_mode:
        info = font.render("Tryb usuwania połączeń: kliknij na linię, aby usunąć (Spacja, aby wyłączyć)", True, RED)
        screen.blit(info, (10, 40))

    # Rysowanie menu jeśli aktywne
    if menu_active:
        pygame.draw.rect(screen, GRAY, (MENU_X, MENU_Y, MENU_WIDTH, MENU_HEIGHT))
        pygame.draw.rect(screen, BLACK, (MENU_X, MENU_Y, MENU_WIDTH, MENU_HEIGHT), 2)

        title = font.render("Menu waypointa", True, BLACK)
        screen.blit(title, (MENU_X + 10, MENU_Y + 10))

        if menu_wp_selected:
            wp_label = font.render(f"Wybrano: {menu_wp_selected}", True, BLACK)
            screen.blit(wp_label, (MENU_X + 10, MENU_Y + 40))

        button_height = 30
        button_margin = 10
        start_y = MENU_Y + 70

        for i, btn in enumerate(buttons):
            rect = pygame.Rect(MENU_X + 10, start_y + i * (button_height + button_margin), MENU_WIDTH - 20, button_height)
            draw_button(screen, rect, btn["label"], active=btn["action"] is not None)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_map("mapa.json", waypoints, connections)
            running = False

        elif event.type == pygame.KEYDOWN:
            if editing_name:
                if event.key == pygame.K_RETURN:
                    new_name = input_text.strip().upper()
                    if new_name == "" or new_name in waypoints:
                        pass
                    else:
                        waypoints[new_name] = waypoints.pop(editing_wp)
                        editing_wp = new_name
                    editing_name = False
                    editing_wp = None
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if event.unicode.isalnum():
                        input_text += event.unicode
            elif event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # lub SCREEN_WIDTH, SCREEN_HEIGHT
            else:
                if event.key == pygame.K_SPACE:
                    if delete_connection_mode:
                        delete_connection_mode = False
                    else:
                        menu_active = not menu_active
                        menu_wp_selected = None

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if editing_name:
                continue

            if menu_active:
                button_height = 30
                button_margin = 10
                start_y = MENU_Y + 70
                clicked_button = None
                for i, btn in enumerate(buttons):
                    rect = pygame.Rect(MENU_X + 10, start_y + i * (button_height + button_margin), MENU_WIDTH - 20, button_height)
                    if rect.collidepoint(pos):
                        clicked_button = btn
                        break

                if clicked_button:
                    if clicked_button["action"] == "delete_wp":
                        if menu_wp_selected:
                            del waypoints[menu_wp_selected]
                            connections = [c for c in connections if menu_wp_selected not in c]
                            menu_wp_selected = None
                    elif clicked_button["action"] == "delete_connections":
                        delete_connection_mode = not delete_connection_mode
                        menu_active = False
                        menu_wp_selected = None
                else:
                    wp_name = get_nearest_waypoint(pos)
                    if wp_name:
                        menu_wp_selected = wp_name
                    else:
                        menu_wp_selected = None

            else:
                if delete_connection_mode:
                    # Kliknięcie w trybie usuwania połączeń — szukamy lini blisko kliknięcia
                    clicked_line = None
                    threshold = 7
                    for a, b in connections:
                        start_pos = (waypoints[a][0] + camera_offset[0], waypoints[a][1] + camera_offset[1])
                        end_pos = (waypoints[b][0] + camera_offset[0], waypoints[b][1] + camera_offset[1])
                        dist = point_line_distance(pos, start_pos, end_pos)
                        if dist < threshold:
                            clicked_line = (a, b)
                            break
                    if clicked_line:
                        connections.remove(clicked_line)
                else:
                    if event.button == 3:
                        default_name = next(name_gen)
                        waypoints[default_name] = (pos[0] - camera_offset[0], pos[1] - camera_offset[1])  # uwzględnij offset przy dodawaniu
                        editing_name = True
                        editing_wp = default_name
                        input_text = ""

                    elif event.button == 1:
                        wp_name = get_nearest_waypoint(pos)
                        if wp_name:
                            if selected is None:
                                selected = wp_name
                            else:
                                if selected != wp_name:
                                    pair = (selected, wp_name)
                                    reverse = (wp_name, selected)
                                    if pair not in connections and reverse not in connections:
                                        connections.append(pair)
                                selected = None

    # Obsługa przesuwania kamery tylko, gdy nie edytujemy nazwy, menu nie jest aktywne i tryb usuwania połączeń wyłączony
    keys = pygame.key.get_pressed()
    if not editing_name and not menu_active and not delete_connection_mode:
        if keys[pygame.K_LEFT]:
            camera_offset[0] += CAMERA_SPEED
        if keys[pygame.K_RIGHT]:
            camera_offset[0] -= CAMERA_SPEED
        if keys[pygame.K_UP]:
            camera_offset[1] += CAMERA_SPEED
        if keys[pygame.K_DOWN]:
            camera_offset[1] -= CAMERA_SPEED

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
