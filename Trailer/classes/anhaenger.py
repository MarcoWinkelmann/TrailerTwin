import pygame
from utils.transformations import rotate_point, translate_along_vector

BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Anhaenger:
    def __init__(self, x, y, laenge, breite, kupplungslaenge, radachsenabstand):
        self.kupplungslaenge = kupplungslaenge
        self.radachsenabstand = radachsenabstand
        self.laenge = laenge
        self.breite = breite
        self.winkel = 0
        self.kupplung = (x, y)
        self.rot_center = (self.kupplung[0] - self.radachsenabstand, self.kupplung[1])
        self.radachse_start = (self.rot_center[0], self.rot_center[1] + self.breite / 2)
        self.radachse_ende = (self.rot_center[0], self.rot_center[1] - self.breite / 2)
        self.top_left = (self.kupplung[0] - self.laenge, self.kupplung[1] - self.breite / 2)
        self.top_right = (self.kupplung[0] - self.kupplungslaenge, self.kupplung[1] - self.breite / 2)
        self.bottom_right = (self.kupplung[0] - self.kupplungslaenge, self.kupplung[1] + self.breite / 2)
        self.bottom_left = (self.kupplung[0] - self.laenge, self.kupplung[1] + self.breite / 2)

    def draw(self, screen):
        # Zeichnen des Anhängerkörpers
        pygame.draw.polygon(screen, BLUE, [self.top_left,self.top_right, self.bottom_right, self.bottom_left])
        # Zeichnen der Achsen
        pygame.draw.line(screen, YELLOW, (self.rot_center[0], self.rot_center[1]), (self.kupplung[0], self.kupplung[1]), 3)
        pygame.draw.line(screen, YELLOW, (self.radachse_start[0], self.radachse_start[1]), (self.radachse_ende[0], self.radachse_ende[1]), 3)
        # Zeichnen der Kreise für Rotationspunkt und Anhängerkupplung
        pygame.draw.circle(screen, GREEN, (self.kupplung[0], self.kupplung[1]), 5)
        pygame.draw.circle(screen, RED, (self.rot_center[0], self.rot_center[1]), 3)

    def rotate(self, delta_angle):
        self.winkel += delta_angle
        # Calculate new hitch position based on the angle
        self.kupplung = rotate_point(self.rot_center[0], self.rot_center[1], self.kupplung[0], self.kupplung[1], delta_angle)
        self.radachse_start = rotate_point(self.rot_center[0], self.rot_center[1], self.radachse_start[0], self.radachse_start[1],delta_angle)
        self.radachse_ende = rotate_point(self.rot_center[0], self.rot_center[1], self.radachse_ende[0], self.radachse_ende[1], delta_angle)
        self.top_left = rotate_point(self.rot_center[0], self.rot_center[1], self.top_left[0], self.top_left[1], delta_angle)
        self.top_right = rotate_point(self.rot_center[0], self.rot_center[1], self.top_right[0], self.top_right[1], delta_angle)
        self.bottom_right = rotate_point(self.rot_center[0], self.rot_center[1], self.bottom_right[0], self.bottom_right[1], delta_angle)
        self.bottom_left = rotate_point(self.rot_center[0], self.rot_center[1], self.bottom_left[0], self.bottom_left[1], delta_angle)

    def translate(self, distance):
        """Translate the trailer forward or backward along the vector between rot_center and kupplung by a given distance"""
        # Calculate new positions for kupplung and rot_center
        new_kupplung_x, new_kupplung_y = translate_along_vector(self.rot_center[0], self.rot_center[1],self.kupplung[0], self.kupplung[1], distance)
        # Update the positions
        delta_x = new_kupplung_x - self.kupplung[0]
        delta_y = new_kupplung_y - self.kupplung[1]

        self.kupplung = (new_kupplung_x, new_kupplung_y)
        self.rot_center = (self.rot_center[0] + delta_x, self.rot_center[1] + delta_y)
        self.radachse_start = (self.radachse_start[0] + delta_x, self.radachse_start[1] + delta_y)
        self.radachse_ende = (self.radachse_ende[0] + delta_x, self.radachse_ende[1] + delta_y)
        self.top_left = (self.top_left[0] + delta_x, self.top_left[1] + delta_y)
        self.top_right = (self.top_right[0] + delta_x, self.top_right[1] + delta_y)
        self.bottom_right = (self.bottom_right[0] + delta_x, self.bottom_right[1] + delta_y)
        self.bottom_left = (self.bottom_left[0] + delta_x, self.bottom_left[1] + delta_y)