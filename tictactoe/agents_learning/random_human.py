# Importar tu clase Tablero
from tablero_gym import Tablero
from error_classes import InvalidInputError, CellOccupiedError
import random

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
cant_eps = 2

for _ in range(cant_eps):
    state, info = env.reset()
    env.render()
    done = False
    truncated = False
    while not done or truncated:
        try:
            action = random.choice(info["valid_actions"])  # Acción aleatoria
            state, reward, done, truncated, info = env.step(action)
            env.render()
        except (InvalidInputError, CellOccupiedError) as e:
            print(f"Se produjo un error: {e}")
            break



env.close()
