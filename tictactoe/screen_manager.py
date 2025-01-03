import pygame # type: ignore
from pygame.locals import * # type: ignore

from button import Button
from constants import WINDOW_SIZE, CELL_SIZE, BUTTON_SIZE, COLORS, get_path, get_font


class ScreenManager:
    """Handles all screen-related operations."""
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()


        # Inicialización de capas
        self.static_layer = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
        self.dynamic_layer = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)

        # Background and Icons
        self.background = pygame.transform.scale(
            pygame.image.load(get_path("images/background/tic-tac-toe-background.jpg")),
            WINDOW_SIZE
        )
        self.img_o = pygame.transform.scale(pygame.image.load(get_path("images/tictactoe/o.png")), (100, 100))
        self.img_x = pygame.transform.scale(pygame.image.load(get_path("images/tictactoe/x.png")), (100, 100))

        # Buttons
        self.buttons = {
            "pvp": Button(
                image=pygame.image.load(get_path("images/buttons/PvP-Rect.png")),
                pos=(540, 200),
                text_input="Player vs Player",
                font=get_font(75),
                base_color="#abf7f2",
                hovering_color=COLORS["white"],
            ),
            "pvb": Button(
                image=pygame.image.load(get_path("images/buttons/PvB-Rect.png")),
                pos=(540, 350),
                text_input="Player vs Bot",
                font=get_font(75),
                base_color="#abf7f2",
                hovering_color=COLORS["white"],
            ),
            "quit": Button(
                image=pygame.image.load(get_path("images/buttons/Quit-Rect.png")),
                pos=(540, 500),
                text_input="Quit",
                font=get_font(75),
                base_color="#abf7f2",
                hovering_color=COLORS["white"],
            ),
        }


    def draw_menu(self, mouse_pos, music_bool):
        """Draws the main menu."""
        self.screen.fill(COLORS["black"])
        self.screen.blit(self.background, (0, 0))
        title = get_font(100).render("Main Menu", True, COLORS["menu_text"])
        self.screen.blit(title, title.get_rect(center=(540, 50)))

        for button in self.buttons.values():
            button.changeColor(mouse_pos)
            button.update(self.screen)

        cond = "ON" if music_bool else "OFF"
        self.__draw_button( f"Music: {cond}", 900, 500, self.screen)


    def __draw_board(self):
        """Draws the tic-tac-toe grid."""
        margin_left = (WINDOW_SIZE[0] - CELL_SIZE * 3) // 2
        margin_top = (WINDOW_SIZE[1] - CELL_SIZE * 3) // 2
        for i in range(1, 3):
            pygame.draw.line(
                self.static_layer, COLORS["red"], 
                (margin_left, margin_top + CELL_SIZE * i),
                (margin_left + CELL_SIZE * 3, margin_top + CELL_SIZE * i), 
                5
            )
            pygame.draw.line(
                self.static_layer, COLORS["red"], 
                (margin_left + CELL_SIZE * i, margin_top),
                (margin_left + CELL_SIZE * i, margin_top + CELL_SIZE * 3), 
                5
            )

    def __draw_button(self, title, x, y, surf):
        #x = 900
        #y sera 100 o 200

        font = get_font(40)
        texto = font.render(title, True, COLORS["white"]) #title: "Reiniciar" o "Volver"

        text_x = x + (BUTTON_SIZE[0] - texto.get_width() )  // 2 
        text_y = y + (BUTTON_SIZE[1] - texto.get_height() )  // 2 

        pygame.draw.rect(surf, COLORS["green"], (x, y, *BUTTON_SIZE))  # Botón
        surf.blit(texto, (text_x, text_y))

    def start_match(self):
        self.static_layer.fill(COLORS["white"])
        self.__draw_button("Reiniciar", 900, 100, self.static_layer)
        self.__draw_button("Volver", 900, 200, self.static_layer)
        self.__draw_board()

    def draw_symbol(self, row, column, turn):
        
        # depende cual cuadrado es, marco el punto del pos_x (300, 490, 670) izquierda a derecha, en aumento 180
        pos_col = 310 
        # depende cual cuadrado es, marco el punto del pos_y (80, 260, 440) arriba hacia abajo, en aumento 180
        pos_row = 80

        pos_x_to_draw = pos_col + (180 * column)
        pos_y_to_draw = pos_row + (180 * row)

        icon_to_draw = self.img_x if turn == 1 else self.img_o
        self.static_layer.blit(icon_to_draw, (pos_x_to_draw, pos_y_to_draw))

        sound_click = pygame.mixer.Sound(get_path("sounds/effect.mp3"))
        sound_click.set_volume(0.6) 
        sound_click.play()






#cuando estas en el tablero muestra de quien es el turno en el mouse (la X o la O)
#se puede ignorar estos metodos, pero para los metodos de arriba habria que cambiar self.static_layer por self.screen_manager
    def update_dynamic(self,turn, mouse_pos):
         # Actualizar la capa dinámica con el cursor

        self.dynamic_layer.fill((0, 0, 0, 0))  # Limpia la capa dinámica
        cursor_img = self.img_x if turn == 1 else self.img_o
        cursor_img =  pygame.transform.scale(cursor_img, (50, 50))
        self.dynamic_layer.blit(cursor_img, 
                              (mouse_pos[0] - cursor_img.get_width()//2,
                               mouse_pos[1] - cursor_img.get_height()//2))

    def update_all_layers(self):
        # Dibujar todas las capas
        self.screen.fill(COLORS["white"])
        self.screen.blit(self.static_layer, (0, 0))
        self.screen.blit(self.dynamic_layer, (0, 0))
