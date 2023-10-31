import pygame
import math
import sys
from classes.anhaenger import Anhaenger

def point_inside_polygon(x, y, poly):
    """Check if a point is inside a polygon."""
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_intersection = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= x_intersection:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Initialize Pygame
pygame.init()

# Window size and color definitions
WIDTH, HEIGHT = 1800, 1200
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pillars = [pygame.Rect(600, 400, 10, 10), pygame.Rect(600, 750, 10, 10), pygame.Rect(850, 400, 10, 10), pygame.Rect(850, 750, 10, 10)]

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Anhänger Simulation")

    mouse_dragging = False

    anhänger = Anhaenger(WIDTH / 2, HEIGHT / 2, 620, 220, 200, 500)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    anhänger.rotate(-0.05)
                elif event.key == pygame.K_RIGHT:
                    anhänger.rotate(0.05)
                elif event.key == pygame.K_UP:
                    anhänger.translate(5)
                elif event.key == pygame.K_DOWN:
                    anhänger.translate(-5)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if math.sqrt((x - anhänger.kupplung[0]) ** 2 + (
                        y - anhänger.kupplung[1]) ** 2) <= 5:  # 5 ist der Radius des grünen Kreises
                    mouse_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_dragging = False
            elif event.type == pygame.MOUSEMOTION and mouse_dragging:
                x, y = pygame.mouse.get_pos()
                # Vektoren definieren
                mouse_vec = (x - anhänger.kupplung[0], y - anhänger.kupplung[1])
                central_vec = (anhänger.kupplung[0] - anhänger.rot_center[0], anhänger.kupplung[1] - anhänger.rot_center[1])
                # Skalarprodukte berechnen
                dot_product = mouse_vec[0] * central_vec[0] + mouse_vec[1] * central_vec[1]
                central_vec_magnitude_squared = central_vec[0] ** 2 + central_vec[1] ** 2
                # Projektion des Mausvektors auf den zentralen Vektor berechnen
                projection_length = dot_product / central_vec_magnitude_squared * math.sqrt(central_vec_magnitude_squared)
                # Projektion des Mausvektors auf die Senkrechte des zentralen Vektors berechnen
                perp_vec = (-central_vec[1], central_vec[0])
                perp_vec_magnitude_squared = perp_vec[0] ** 2 + perp_vec[1] ** 2
                d_perp = mouse_vec[0] * perp_vec[0] + mouse_vec[1] * perp_vec[1]
                perp_projection_length = d_perp / perp_vec_magnitude_squared * math.sqrt(perp_vec_magnitude_squared)
                # Winkel berechnen
                delta_angle = math.atan2(perp_projection_length, projection_length + anhänger.radachsenabstand)
                # Anhänger aktualisieren
                anhänger.translate(projection_length)
                anhänger.rotate(delta_angle)

        screen.fill(WHITE)
        anhänger.draw(screen)

        for pillar in pillars:
            pygame.draw.rect(screen, RED, pillar)

        trailer_polygon = [anhänger.top_left, anhänger.kupplung, anhänger.top_right, anhänger.bottom_right, anhänger.bottom_left, anhänger.top_left]
        collision_detected = False

        for pillar in pillars:
            for vertex in [(pillar.left, pillar.top), (pillar.right, pillar.top), (pillar.left, pillar.bottom),
                           (pillar.right, pillar.bottom)]:
                if point_inside_polygon(vertex[0], vertex[1], trailer_polygon):
                    collision_detected = True
                    break

        if collision_detected:
            screen.fill(RED)  # Füllt den Bildschirm mit Rot
            anhänger.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
