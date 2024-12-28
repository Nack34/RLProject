# Importar tu clase Tablero
from tablero_gym import Tablero

# Crear una instancia del entorno
env = Tablero()
'''
# Usar el entorno
state, _ = env.reset()
env.render()

# Realizar una acción
action = (0,1)  # Ejemplo: marcar la primera celda
obs, reward, done, truncated, info = env.step(action)
env.render()

'''
for _ in range(2):
    state, _ = env.reset()
    env.render()
    done = False
    truncated = False
    while not done or truncated:
        action = env.action_space.sample()  # Acción aleatoria
        state, reward, done, truncated, _ = env.step(action)
        env.render()


env.close()
