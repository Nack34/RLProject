import pygame, sys
from pygame.locals import *

pygame.init()
#tamaño de la ventana
ancho_ventana= 1080
alto_ventana= 600
PANTALLA = pygame.display.set_mode((ancho_ventana,alto_ventana))

FPS = 60
RELOJ = pygame.time.Clock()

#imagenes de fondo
back = pygame.image.load("images/background/parallax-forest-back-trees.png")
front = pygame.image.load("images/background/parallax-forest-front-trees.png")
lights = pygame.image.load("images/background/parallax-forest-lights.png")
middle = pygame.image.load("images/background/parallax-forest-middle-trees.png")

# Redimensionar las imágenes para que ocupen toda la pantalla
back = pygame.transform.scale(back, (ancho_ventana, alto_ventana))
front = pygame.transform.scale(front, (ancho_ventana, alto_ventana))
middle = pygame.transform.scale(middle, (ancho_ventana, alto_ventana))
lights = pygame.transform.scale(lights, (ancho_ventana, alto_ventana))

x_background=0
y_background=0

background = [(back,(x_background,y_background)),(lights,(x_background,y_background)), (middle,(x_background,y_background)),(front,(x_background,y_background))]
PANTALLA.blits(background)

#Ventana
pygame.display.set_caption("Guerrero")
icono = pygame.image.load("images/icons/icono_ventana.png")
pygame.display.set_icon(icono)

VERDE = (0,255,0)
AZUL = (0,0,255)
ROJO = (255,0,0)
NEGRO = (0,0,0)
BLANCO = (255,255,255)
CELESTE = (23,227,217)




def play_back_ground():
    global x_background
    global y_background
    x_relative = (x_background % ancho_ventana) # para no desfasar del ancho de la ventana la x (para que vuelva a empezar)
    background = [(back, (x_relative - ancho_ventana, y_background)), (lights, (x_relative - ancho_ventana, y_background)), (middle, (x_relative - ancho_ventana, y_background)), (front, (x_relative - ancho_ventana, y_background))]
    PANTALLA.blits(background)
    if x_relative < ancho_ventana:
        background = [(back, (x_relative, y_background)), (lights, (x_relative , y_background)),
                    (middle, (x_relative, y_background)), (front, (x_relative, y_background))]
        PANTALLA.blits(background)

    x_background -= 1

def play_game():
    # Detectar clics del mouse
    if event.type == pygame.MOUSEBUTTONDOWN:
        print(f"Clic detectado en {event.pos}, botón: {event.button}")
        



while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    play_back_ground()
    play_game()


    pygame.display.update()
    RELOJ.tick(FPS)
