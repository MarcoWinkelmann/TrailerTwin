import math

def rotate_point(cx, cy, x, y, angle):
    """Rotate point (x,y) around point (cx,cy) by a specific angle."""
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)

    # Translate point to origin
    x -= cx
    y -= cy

    # Rotate point
    x_new = x * cos_a - y * sin_a
    y_new = x * sin_a + y * cos_a

    # Translate point back
    x_new += cx
    y_new += cy

    return x_new, y_new

def translate_along_vector(cx, cy, hx, hy, distance):
    """Translate point (hx, hy) by a given distance along the vector formed with (cx, cy)"""
    vector_length = math.sqrt((hx - cx)**2 + (hy - cy)**2)
    normalized_x = (hx - cx) / vector_length
    normalized_y = (hy - cy) / vector_length

    new_x = hx + normalized_x * distance
    new_y = hy + normalized_y * distance

    return new_x, new_y
