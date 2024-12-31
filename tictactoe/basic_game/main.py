import random
import pygame, sys # type: ignore
from pygame.locals import * # type: ignore
from config import init_game, VERDE, ROJO, BLANCO, NEGRO
from button import Button
from tablero import Tablero
from tensorflow.keras.models import load_model
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from error_classes import InvalidInputError, CellOccupiedError


PANTALLA, FPS, RELOJ, img_o, img_x, fondo = init_game(pygame)


def manejar_evento_cerrar():
    pygame.quit()
    sys.exit()
    pygame.mixer.music.stop()


def pintar(tablero, turno, columna, fila, img_x, img_o, PANTALLA):
    pos_x_to_draw, pos_y_to_draw= tablero.get_pos_pintar(columna, fila)
    icon_to_draw = img_x if turno == 1 else img_o
    PANTALLA.blit(icon_to_draw, (pos_x_to_draw, pos_y_to_draw))


def check_reset(event):
    clic_x, clic_y = event.pos

    if 900 <= clic_x <= 1050 and 100 <= clic_y <= 150:
        return True
    return False

def check_exit(event):
    clic_x, clic_y = event.pos

    if 900 <= clic_x <= 1050 and 200 <= clic_y <= 250:
        return True
    return False



def draw_tic_tac_toe_board():
    # Tamaño de cada celda
    cell_size = 180

    # Calcula los márgenes para centrar el tablero
    margin_left = (1080 - cell_size * 3) // 2  # 270 píxeles
    margin_top = (600 - cell_size * 3) // 2  # 30 píxeles

    # Dibuja las líneas horizontales
    for i in range(1, 3):  # Dos líneas horizontales
        pygame.draw.line(PANTALLA, ROJO, (margin_left, margin_top + cell_size * i),
                         (margin_left + cell_size * 3, margin_top + cell_size * i), 5)

    # Dibuja las líneas verticales
    for i in range(1, 3):  # Dos líneas verticales
        pygame.draw.line(PANTALLA, ROJO, (margin_left + cell_size * i, margin_top),
                         (margin_left + cell_size * i, margin_top + cell_size * 3), 5)

def draw_reset_button():
    pygame.draw.rect(PANTALLA, VERDE, (900, 100, 150, 50))  # Botón
    font = pygame.font.SysFont(None, 40)
    texto = font.render("Reiniciar", True, BLANCO)
    PANTALLA.blit(texto, (910, 110))

def draw_exit_button():
    pygame.draw.rect(PANTALLA, VERDE, (900, 200, 150, 50))  # Botón
    font = pygame.font.SysFont(None, 40)
    texto = font.render("Volver", True, BLANCO)
    PANTALLA.blit(texto, (930, 210))


def start_match(PANTALLA, BLANCO):
    PANTALLA.fill(BLANCO)
    draw_reset_button()
    draw_exit_button()
    draw_tic_tac_toe_board()

    tablero = Tablero()
    turno = 1
    termino = False

    return (tablero, turno, termino)

#intent mio
def player_vs(img_x, img_o, PANTALLA, BLANCO, vsBot, model_name = None):
    def get_bot_choice(env, model=None):
        valid_actions = env.get_libres()
        if model is None:
            return random.choice(valid_actions)
        else:
            state = np.array(env.tablero)
            q_values = model.predict(state.reshape(1, 3, 3), verbose=0)
            flat_index = np.argmax(q_values)
            action = [flat_index // 3, flat_index % 3]

            # Verificar si la acción es válida
            if action not in valid_actions:
                action = random.choice(valid_actions)  # Si no es válida, tomar una acción aleatoria
            
            return action
    
    
    model = None if model_name is None else load_model("../agents_learning/training/"+model_name)

    title = "PvB" if vsBot else "PvP"     
    pygame.display.set_caption(title)

    tablero, turno, termino = start_match(PANTALLA, BLANCO)
    seguir_jugando = True 

    # crear evento manual
    EJECUTAR_FUNCION = pygame.USEREVENT + 1

    # Bandera para saber si el temporizador está activo
    temporizador_activo = False
    
    while seguir_jugando:
        for event in pygame.event.get():
            if event.type == QUIT: #type: ignore
                manejar_evento_cerrar()
            
            if event.type == pygame.MOUSEBUTTONDOWN and ( (not vsBot) or (vsBot and not temporizador_activo ) ):
                if check_reset(event):
                    tablero, turno, termino = start_match(PANTALLA, BLANCO)

                elif check_exit(event):
                    seguir_jugando = False

                elif not termino:
                    try:
                        clic_x, clic_y = event.pos
                        
                        columna = tablero.get_columna(clic_x)
                        fila = tablero.get_fila(clic_y)

                        termino = tablero.marcar(turno, columna, fila)

                        pintar(tablero, turno, columna, fila, img_x, img_o, PANTALLA)
                        
                        #changing turn
                        if not termino:
                            turno = 2 if turno == 1 else 1
                            if vsBot:
                                pygame.time.set_timer(EJECUTAR_FUNCION, 1000)  # Inicia el temporizador
                                temporizador_activo = True

                    except (InvalidInputError, CellOccupiedError) as e:
                        print(e)

            if vsBot and event.type == EJECUTAR_FUNCION and temporizador_activo:
                fila, columna = get_bot_choice(tablero, model)

                # Ejecuta la función cuando se activa el temporizador (marcar aleatorio)
                termino = tablero.marcar(turno, columna, fila)
                
                pintar(tablero, turno, columna, fila, img_x, img_o, PANTALLA)
                    
                # Detiene el temporizador
                pygame.time.set_timer(EJECUTAR_FUNCION, 0)
                temporizador_activo = False

                #changing turn
                if not termino:
                    turno = 2 if turno == 1 else 1

               
        pygame.display.update()
        RELOJ.tick(FPS)



def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(None, size)

def main_menu(): # main menu screen
    while True:
        PANTALLA.fill(NEGRO)
        pygame.display.set_caption("Tictactoe")
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        MENU_TXT = get_font(100).render("Main Menu", True, "#30d1cc")
        MENU_RECT = MENU_TXT.get_rect(center = (540, 50)) #Probar centralizado

        PVP_BUTTON = Button(image = pygame.image.load("../images/buttons/PvP-Rect.png"), pos = (540, 200), 
                            text_input = "Player vs Player", font = get_font(75), base_color = "#abf7f2", hovering_color = BLANCO)
        PVB_BUTTON = Button(image = pygame.image.load("../images/buttons/PvB-Rect.png"), pos = (540, 350),
                            text_input = "Player vs Bot", font = get_font(75), base_color = "#abf7f2", hovering_color = BLANCO)
        QUIT_BUTTON = Button(image = pygame.image.load("../images/buttons/Quit-Rect.png"), pos = (540, 500), 
                             text_input = "Quit", font = get_font(75), base_color = "#abf7f2", hovering_color = BLANCO)

        PANTALLA.blit(fondo, (0, 0))
        PANTALLA.blit(MENU_TXT, MENU_RECT)

        for button in [PVP_BUTTON, PVB_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(PANTALLA)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                manejar_evento_cerrar()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PVP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player_vs(img_x, img_o, PANTALLA, BLANCO, False)
                if PVB_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player_vs(img_x, img_o, PANTALLA, BLANCO, True, model_name="monte_carlo_model_v5.keras")
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    manejar_evento_cerrar()
        pygame.display.update()


main_menu()