import pygame
import gymnasium as gym

# Inicializar pygame
pygame.init()

# Crear el entorno de Gymnasium
env = gym.make('CartPole-v1', render_mode='rgb_array')
env.reset()

# Dimensiones de la ventana
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CartPole-v1")

# Reloj para controlar FPS
clock = pygame.time.Clock()
fps = 30

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paso del entorno (acción aleatoria)
    action = env.action_space.sample()  # Elegir acción aleatoria
    observation, reward, done, truncated, info = env.step(action)

    # Renderizar el entorno y convertirlo en una superficie de pygame
    frame = env.render()
    frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # Girar el frame

    # Dibujar el frame en la ventana
    screen.blit(pygame.transform.scale(frame_surface, (screen_width, screen_height)), (0, 0))
    pygame.display.flip()

    # Reiniciar el entorno si termina
    if done:
        pass
        #env.reset() # TODO: ACA TENDRIA QUE ESTAR EL RESET, LO COMENTE PARA QUE SE VEA QUE NO HAY UN MODELO DE IA ENTRENADO

    clock.tick(fps)

# Cerrar el entorno y pygame
env.close()
pygame.quit()
