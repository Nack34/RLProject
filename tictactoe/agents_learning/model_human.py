# Importar las bibliotecas necesarias
from tensorflow.keras.models import load_model
from tablero_gym import Tablero
from error_classes import InvalidInputError, CellOccupiedError
import random
import numpy as np

model_name = "monte_carlo_model.keras"

# Cargar el modelo guardado
model = load_model("training/"+model_name)

# Crear una instancia del entorno
env = Tablero()
cant_eps = 2

for _ in range(cant_eps):
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

env.close()
