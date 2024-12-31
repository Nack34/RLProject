# Importar las bibliotecas necesarias
from tensorflow.keras.models import load_model
from tablero_gym import Tablero
from error_classes import InvalidInputError, CellOccupiedError
import random
import numpy as np

model_name = "monte_carlo_model_v2.keras"

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
            q_values = model.predict(state.reshape(1, 3, 3), verbose=0)
            flat_index = np.argmax(q_values)
            action = [flat_index // 3, flat_index % 3]

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
print(f"Total de partidas: {total_partidas}")
print(f"Cantidad de partidas ganadas por X: {wins_x}")
print(f"Cantidad de partidas ganadas por O: {wins_o}")
print(f"Empates: {draws}")
print(f"Porcentaje de partidas ganadas por X: {wins_x/total_partidas}")
print(f"Porcentaje de partidas ganadas por O: {wins_o/total_partidas}")
print(f"Porcentaje de empates: {draws/total_partidas}")
print()
print()
