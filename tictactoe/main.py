import pygame, sys # type: ignore
from pygame.locals import * # type: ignore
from error_classes import InvalidInputError, CellOccupiedError
from config import init_game, VERDE, ROJO, BLANCO, NEGRO
from button import Button
from classes import Tablero

PANTALLA, FPS, RELOJ, img_o, img_x, fondo = init_game(pygame)



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



#intent mio
def player_vs_bot(img_x, img_o, PANTALLA):
    pygame.display.set_caption("PvB")    

    PANTALLA.fill(BLANCO)
    draw_reset_button()
    draw_exit_button()
    draw_tic_tac_toe_board()

    tablero = Tablero(img_x, img_o)
    turno = 1
    seguir_jugando = True
    
    EJECUTAR_FUNCION = pygame.USEREVENT + 1

    # Bandera para saber si el temporizador está activo
    temporizador_activo = False

    player_jugo = False
    termino =  False


    while seguir_jugando:
        for event in pygame.event.get():

            if event.type == QUIT: #type: ignore
                pygame.quit()
                sys.exit()
                pygame.mixer.music.stop()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_reset(event) and not temporizador_activo:
                    PANTALLA.fill(BLANCO)
                    draw_reset_button()
                    draw_exit_button()
                    draw_tic_tac_toe_board()
                    tablero = Tablero(img_x, img_o)
                    turno = 1
                    termino = False
                    player_jugo = False

                elif check_exit(event) and not temporizador_activo:
                    seguir_jugando = False

                elif  not player_jugo and not termino and not temporizador_activo:
                    try:
                        clic_x, clic_y = event.pos
                        
                        termino = tablero.marcar(turno, clic_x, clic_y, PANTALLA)
                        player_jugo = True
                        #changing turn
                        if not termino:
                            turno = 2 if turno == 1 else 1 
                            pygame.time.set_timer(EJECUTAR_FUNCION, 1000)  # Inicia el temporizador
                            temporizador_activo = True
                            print("Temporizador activado.")

                    except (InvalidInputError, CellOccupiedError) as e:
                        print(e)


            if event.type == EJECUTAR_FUNCION and temporizador_activo:
                print("llegue2")
                # Ejecuta la función cuando se activa el temporizador
                termino = tablero.marcar_aleatorio(turno, PANTALLA)
                # Detiene el temporizador
                pygame.time.set_timer(EJECUTAR_FUNCION, 0)
                temporizador_activo = False
                player_jugo = False
                if not termino:
                    turno = 2 if turno == 1 else 1 

               
        pygame.display.update()
        RELOJ.tick(FPS)

def player_vs_player(img_x, img_o, PANTALLA):
    pygame.display.set_caption("PvP")    

    PANTALLA.fill(BLANCO)
    draw_reset_button()
    draw_exit_button()
    draw_tic_tac_toe_board()

    tablero = Tablero(img_x, img_o)
    turno = 1
    seguir_jugando = True
    termino = False

    while seguir_jugando:
        for event in pygame.event.get():

            if event.type == QUIT: #type: ignore
                pygame.quit()
                sys.exit()
                pygame.mixer.music.stop()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_reset(event):
                    PANTALLA.fill(BLANCO)
                    draw_reset_button()
                    draw_exit_button()
                    draw_tic_tac_toe_board()
                    tablero = Tablero(img_x, img_o)
                    turno = 1
                    termino = False

                elif check_exit(event):
                    seguir_jugando = False

                elif not termino:
                    try:
                        clic_x, clic_y = event.pos
                        
                        termino = tablero.marcar(turno, clic_x, clic_y, PANTALLA)
                        #changing turn
                        if not termino:
                            turno = 2 if turno == 1 else 1

                    except (InvalidInputError, CellOccupiedError) as e:
                        print(e)


               
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

        PVP_BUTTON = Button(image = pygame.image.load("images/buttons/PvP-Rect.png"), pos = (540, 200), 
                            text_input = "Player vs Player", font = get_font(75), base_color = "#abf7f2", hovering_color = BLANCO)
        PVB_BUTTON = Button(image = pygame.image.load("images/buttons/PvB-Rect.png"), pos = (540, 350),
                            text_input = "Player vs Bot", font = get_font(75), base_color = "#abf7f2", hovering_color = BLANCO)
        QUIT_BUTTON = Button(image = pygame.image.load("images/buttons/Quit-Rect.png"), pos = (540, 500), 
                             text_input = "Quit", font = get_font(75), base_color = "#abf7f2", hovering_color = BLANCO)

        PANTALLA.blit(fondo, (0, 0))
        PANTALLA.blit(MENU_TXT, MENU_RECT)

        for button in [PVP_BUTTON, PVB_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(PANTALLA)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PVP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player_vs_player(img_x, img_o, PANTALLA)
                if PVB_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player_vs_bot(img_x, img_o, PANTALLA)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


main_menu()