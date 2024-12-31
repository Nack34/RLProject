# Importar las bibliotecas necesarias
from tensorflow.keras.models import load_model
from tablero_gym import Tablero
from error_classes import InvalidInputError, CellOccupiedError
import random
import numpy as np

from training.monte_carlo_v7_1 import model_name 
from training.monte_carlo_v7_1 import model_predict

# Cargar el modelo guardado
model = load_model("training/"+model_name)

# Crear una instancia del entorno
env = Tablero()
cant_eps = 100

draws = 0
wins_x = 0
wins_o = 0

for episode_number in range(cant_eps):
    print(f"Episode: {episode_number}/{cant_eps}")
    state, info = env.reset()
    env.render()
    done = False
    truncated = False
    while not done or truncated:
        try:
            # Usar el modelo para predecir la acción
            action = model_predict(model, state.reshape(1, 3, 3), info["valid_actions"])

            # Verificar si la acción es válida
            if action not in info["valid_actions"]:
                action = random.choice(info["valid_actions"])  # Si no es válida, tomar una acción aleatoria

            # Realizar el paso en el entorno
            state, reward, done, truncated, info = env.step(action)
            env.render()
        except (InvalidInputError, CellOccupiedError) as e:
            print(f"Se produjo un error: {e}")
            break
    draws+= 1 if info["winner"] == 0 else 0
    wins_x+= 1 if info["winner"] == 1 else 0
    wins_o+= 1 if info["winner"] == 2 else 0

env.close()

total_partidas=wins_x+wins_o+draws
print(f"Recapitulacion: \n")
print(f"Total de partidas validas: {total_partidas}/{cant_eps} -> ({(total_partidas/cant_eps)*100})%")
print(f"Ganadas por X: {wins_x}/{total_partidas} -> {(wins_x/total_partidas)*100}%")
print(f"Ganadas por O: {wins_o}/{total_partidas} -> {(wins_o/total_partidas)*100}%")
print(f"Termino empate: {draws}/{total_partidas} -> {(draws/total_partidas)*100}%")
print()
print()
