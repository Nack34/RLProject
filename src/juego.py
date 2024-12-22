import pygame, sys # type: ignore
from pygame.locals import * # type: ignore
from error_classes import InvalidInputError, CellOccupiedError
from config import init_game, VERDE, ROJO, BLANCO

PANTALLA, FPS, RELOJ, img_o, img_x = init_game(pygame)

# variables globales

tablero = [
    [0,0,0], 
    [0,0,0], 
    [0,0,0]
    ]

# saber quien va, saber si tenes q reiniciar por ganar o ocupar todos los recuadros
turno = 1 #1 == x; 2 == o
limpiar = False
cont = 0
debo_reiniciar = False


# depende cual cuadrado es, marco el punto del pos_x (300, 490, 670) izquierda a derecha, en aumento 180
pos_col = 310 
# depende cual cuadrado es, marco el punto del pos_y (80, 260, 440) arriba hacia abajo, en aumento 180
pos_fil = 80



#mov vertical (sector arr,med,abj)
def get_fila(clic_y):
    fila = None
    if 35 <= clic_y <= 205:
        fila = 0
    elif 215 <= clic_y <= 385:
        fila = 1
    elif 395 <= clic_y <= 565:
        fila = 2

    return fila

#mov horizontal (sector izq,med,der)
def get_columna(clic_x):
    col = None
    if 275 <= clic_x <= 445:
        col = 0
    elif 455 <= clic_x <= 625:
        col = 1
    elif 635 <= clic_x <= 805:
        col = 2
    
    return col


def check_player_win(tablero, turno):
    # Verificar filas
    for fila in range(3):
        if all(celda == turno for celda in tablero[fila]):
            return True

    # Verificar columnas
    for columna in range(3):
        if all(tablero[fila][columna] == turno for fila in range(3)):
            return True

    # Verificar diagonal principal
    if all(tablero[i][i] == turno for i in range(3)):
        return True

    # Verificar diagonal secundaria
    if all(tablero[i][2 - i] == turno for i in range(3)):
        return True

    # Si no hay ganador
    return False


def play_game(fila, columna):
    global tablero
    global turno
    global cont
    global debo_reiniciar

    global pos_fil
    global pos_col

    # general checking
    if debo_reiniciar:
        return
    
    if fila is None or columna is None:
        raise InvalidInputError("No le pegaste a nada, negro")
    
    if tablero[fila][columna] != 0:
        raise CellOccupiedError("Ya está ocupado, negro usurero")


    #updating internal structure
    tablero[fila][columna] = turno


    #start to updating screen to ther player
    icon_to_draw = img_x if turno == 1 else img_o


    pos_x_to_draw = pos_col + (180 * columna)
    pos_y_to_draw = pos_fil + (180 * fila)


    PANTALLA.blit(icon_to_draw, (pos_x_to_draw, pos_y_to_draw))


    #checking if player has won
    if check_player_win(tablero, turno):
        turno = 2 if turno == 1 else 1
        debo_reiniciar = True
        return



    cont += 1
    if cont == 9:
        debo_reiniciar = True
    

    turno = 2 if turno == 1 else 1


def check_reset(event):
    global tablero
    global debo_reiniciar
    global limpiar
    global cont

    clic_x, clic_y = event.pos

    if 900 <= clic_x <= 1050 and 100 <= clic_y <= 150:
        tablero = [ [0,0,0], [0,0,0], [0,0,0] ]
        limpiar = True
        debo_reiniciar = False
        cont = 0

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

# already all configured, show all draws on display
PANTALLA.fill(BLANCO)
draw_reset_button()
draw_tic_tac_toe_board()

while True:
    for event in pygame.event.get():
        if event.type == QUIT: # type: ignore
            pygame.quit()
            sys.exit()
            pygame.mixer.music.stop()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            clic_x, clic_y = event.pos
            fila = get_fila(clic_y)
            columna = get_columna(clic_x)

            try:
                play_game(fila, columna)
            except (InvalidInputError, CellOccupiedError) as e:
                print(e)

            check_reset(event)

    if limpiar:
        PANTALLA.fill(BLANCO)
        draw_reset_button()
        draw_tic_tac_toe_board()
        limpiar = False

    pygame.display.update()
    RELOJ.tick(FPS)
