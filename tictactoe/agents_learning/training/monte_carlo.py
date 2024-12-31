from tensorflow.keras import layers, models
import numpy as np
import random
from tablero_gym import Tablero

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

def generate_episode(env):
    state, info = env.reset()
    done = False
    episode_memory = []
    
    while not done:
        # Monte Carlo e-greedy
        if random.uniform(0, 1) < epsilon:
            action = random.choice(info["valid_actions"])
        else:
            q_values = model.predict(state.reshape(1, 3, 3), verbose=0)
            flat_index = np.argmax(q_values)
            action = [flat_index // 3, flat_index % 3]
            if action not in info["valid_actions"]:
                action = random.choice(info["valid_actions"])
        
        next_state, reward, done, _, info = env.step(action)
        episode_memory.append((state, action, reward))
        state = next_state

    return episode_memory

for _ in range(episodes):
    episode = generate_episode(env)
    
    # Actualizar los valores Q usando Monte Carlo
    G = 0
    for t in reversed(range(len(episode))):
        state_t, action_t, reward_t = episode[t]
        G = reward_t + gamma * G
        flat_index = action_t[0] * 3 + action_t[1]
        target = model.predict(state_t.reshape(1, 3, 3), verbose=0)
        target[0][flat_index] = G
        model.fit(state_t.reshape(1, 3, 3), target, verbose=0)
    
    # Reducir epsilon
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

env.close()
