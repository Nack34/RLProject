import os
import pygame # type: ignore
from pygame.locals import * # type: ignore


# Constants
FPS = 60
WINDOW_SIZE = (1080, 600)
CELL_SIZE = 180
BUTTON_SIZE = (150, 50)
COLORS = {
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "red": (255, 0, 0),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "cyan": (23, 227, 217),
    "menu_text": "#30d1cc",
}



# Utility Functions
def get_path(dir_name):
    """Get the full path for the given directory or file."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), dir_name)


def get_font(size):
    """Returns a Pygame font object with the given size."""
    return pygame.font.Font(None, size)



#mov vertical (sector arr,med,abj)
def get_row(clic_y):
    row = -1
    if 35 <= clic_y <= 205:
        row = 0
    elif 215 <= clic_y <= 385:
        row = 1
    elif 395 <= clic_y <= 565:
        row = 2

    return row

#mov horizontal (sector izq,med,der)
def get_column(clic_x):
    col = -1
    if 275 <= clic_x <= 445:
        col = 0
    elif 455 <= clic_x <= 625:
        col = 1
    elif 635 <= clic_x <= 805:
        col = 2
    
    return col

#reset and back btns start both in x= 900 but y = 100 and the other one starts in y = 200
def check_button(event, start_x, start_y):
    clic_x, clic_y = event.pos
    if (start_x <= clic_x <= start_x + BUTTON_SIZE[0]) and (start_y <= clic_y <= start_y + BUTTON_SIZE[1]):
        return True
    return False
