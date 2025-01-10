from tensorflow.keras import layers, models
import tensorflow_probability as tfp
import numpy as np
import random
from optimal_policy import OptimalPolicy

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tablero_gym import Tablero


model_name = "monte_carlo_model_v8_1.keras"

def model_predict(model, state, valid_actions):
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
    
    logits = model(state)  # Obtén los logits desde el modelo
    
    # Aplicar la máscara para las acciones no válidas
    masked_logits = mask_invalid_actions(logits[0].numpy(), valid_actions)  
    
    # Crear la distribución Categorical con los logits enmascarados
    action_distribution = tfp.distributions.Categorical(logits=masked_logits)
    
    flat_index = action_distribution.sample().numpy()

    return [flat_index // 3, flat_index % 3]


def main():

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
    episodes = 10000

    # Crear el ambiente
    env = Tablero()
    env._penalizacion_por_tiempo = 0


    def generate_episode(env):
        def penalize_game_loss(episode): # vamos a probar sin penalizar
            last_step = list(episode[-1])  
            last_step[2] = -5  
            episode[-1] = tuple(last_step)
        
        state, info = env.reset()
        opponent = OptimalPolicy(1) if np.all(state == 0) else OptimalPolicy(2)
        oponent_id = opponent._player.id
        
        print(f"First State:")
        env.render()
        
        valid_actions = info["valid_actions"]
        opponent_action = opponent.model_predict(None, state=state, valid_actions=valid_actions)
        state, reward, done, _, info = env.step(opponent_action)

        episode_memory = []
        
        while not done:
            valid_actions = info["valid_actions"]

            # Monte Carlo e-greedy
            if random.uniform(0, 1) < epsilon:
                action = random.choice(valid_actions)
            else:
                action = model_predict(model, state.reshape(1, 3, 3), valid_actions)

            next_state, reward, done, _, info = env.step(action)
            episode_memory.append((state, action, reward))
            state = next_state

            if not done:
                valid_actions = info["valid_actions"]
                opponent_action = opponent.model_predict(None, state=state, valid_actions=valid_actions)
                state, reward, done, _, info = env.step(opponent_action)

        if info["winner"] == oponent_id:
            penalize_game_loss(episode_memory)
            
        print(f"Last State:")
        env.render()
        print()
        print()
            
        return episode_memory, state, info

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
        episode, last_state, last_info = generate_episode(env)
        
        # Actualizar los valores Q usando Monte Carlo
        actualizacion_monte_carlo(episode)
        
        # Reducir epsilon
        epsilon = max(min_epsilon, epsilon * epsilon_decay)

    env.close()

    model.save(model_name)


if __name__ == "__main__":
    main()
