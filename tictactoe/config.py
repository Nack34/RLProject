VERDE = (0,255,0)
AZUL = (0,0,255)
ROJO = (255,0,0)
NEGRO = (0,0,0)
BLANCO = (255,255,255)
CELESTE = (23,227,217)

def init_game(pygame):
    pygame.init()

    #tamaño de la ventana
    ancho_ventana= 1080
    alto_ventana= 600
    PANTALLA = pygame.display.set_mode((ancho_ventana,alto_ventana))

    FPS = 60
    RELOJ = pygame.time.Clock()

    #Ventana
    pygame.display.set_caption("Tictactoe")
    icono = pygame.image.load("images/icons/icono_ventana.png")
    pygame.display.set_icon(icono)

    #bg
    fondo = pygame.image.load("images/background/tic-tac-toe-background.jpg")
    fondo = pygame.transform.scale(fondo, (ancho_ventana, alto_ventana))

    #add icons to play
    img_o = pygame.image.load("images/tictactoe/o.png")
    img_x = pygame.image.load("images/tictactoe/x.png")

    img_o = pygame.transform.scale(img_o, (100, 100))
    img_x = pygame.transform.scale(img_x, (100, 100))


    #add & config audio
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/loop.mp3")

    # (-1 indica bucle infinito)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

    return (PANTALLA, FPS, RELOJ, img_o, img_x, fondo)

