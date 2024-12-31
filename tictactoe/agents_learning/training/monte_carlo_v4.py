from tensorflow.keras import layers, models
import numpy as np
import random

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tablero_gym import Tablero
from error_classes import InvalidInputError, CellOccupiedError

# Definir el modelo
model = models.Sequential([
    layers.Flatten(input_shape=(3, 3)),
    layers.Dense(64, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(9, activation='linear')  # 9 posibles acciones (3x3 tablero)
])

# Compilar el modelo
model.compile(optimizer='adam', loss='mse')

# Parámetros del aprendizaje
gamma = 0.99  # Factor de descuento
epsilon = 1.0  # Probabilidad de exploración
epsilon_decay = 0.99
min_epsilon = 0.1
episodes = 1000

# Crear el ambiente
env = Tablero()

def generate_episode(env): #TODO: QUE NO SEA SOLO 1, QUE SEAN 2 QUE COMPITAN (pero que sea en realidad 1)
    def penalize_game_loss(episode):
        last_step = list(episode[-1])  
        last_step[2] = -5  
        episode[-1] = tuple(last_step)

    
    def mask_invalid_actions(q_values, valid_actions):
        """
        Aplica una máscara para las acciones no válidas.
        - q_values: array con los valores Q para todas las acciones.
        - valid_actions: lista de acciones válidas en forma de [fila, columna].
        """
        mask = np.full(q_values.shape, -np.inf)  # Inicializar con -inf para acciones inválidas
        for action in valid_actions:
            flat_index = action[0] * 3 + action[1]
            mask[flat_index] = q_values[flat_index]
        return mask
    
    state, info = env.reset()
    done = False
    episode_memory_x = []
    episode_memory_o = []
    
    while not done:
        valid_actions = info["valid_actions"]

        # Monte Carlo e-greedy
        if random.uniform(0, 1) < epsilon:
            action = random.choice(valid_actions)
        else:
            q_values = model.predict(state.reshape(1, 3, 3), verbose=0)[0]
            masked_q_values = mask_invalid_actions(q_values, valid_actions)
            flat_index = np.argmax(masked_q_values)
            action = [flat_index // 3, flat_index % 3]


        next_state, reward, done, _, info = env.step(action)
        if (env.turno_x):
            episode_memory_x.append((state, action, reward))
        else:
            episode_memory_o.append((state, action, reward))

        state = next_state
    
    if info["winner"] == 1:
        penalize_game_loss(episode_memory_x)
    elif info["winner"] == 2:
        penalize_game_loss(episode_memory_o)
        
    return episode_memory_x, episode_memory_o, state, info

def actualizacion_monte_carlo(episode):
    G = 0
    for t in reversed(range(len(episode))):
        state_t, action_t, reward_t = episode[t]
        G = reward_t + gamma * G
        flat_index = action_t[0] * 3 + action_t[1]
        target = model.predict(state_t.reshape(1, 3, 3), verbose=0)
        target[0][flat_index] = G
        model.fit(state_t.reshape(1, 3, 3), target, verbose=0)

for episode_number in range(episodes):
    print(f"Episode: {episode_number}/{episodes}")
    episode_x, episode_o, last_state, last_info = generate_episode(env)
    print(f"Last State:")
    env.render()
    print()
    print()
    
    # Actualizar los valores Q usando Monte Carlo
    actualizacion_monte_carlo(episode_x)
    actualizacion_monte_carlo(episode_o)
    
    # Reducir epsilon
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

env.close()

model.save("monte_carlo_model_v4.keras")
