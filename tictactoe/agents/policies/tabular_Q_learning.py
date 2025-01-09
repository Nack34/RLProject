import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tablero_gym import Tablero

model_name = "tabular_Q_learning"

def optimal_policy(Qtable, state):
  # Exploitation: take the action with the highest state, action value
  action = np.argmax(Qtable[state][:])
  return action

def initialize_q_table(state_space, action_space):
    Qtable = np.zeros((state_space, action_space))
    return Qtable

def greedy_policy(Qtable, state):
  # Exploitation: take the action with the highest state, action value
  action = np.argmax(Qtable[state][:])
  return action

def main(): #TODO: Basarme en el curso de hugging face
    # Crear el ambiente
    env = Tablero()
    env._penalizacion_por_tiempo = 0
    env._recompensa_ganar = 1

    #TODO: Modificar el ambiente para que se pueda usar el .n en 
    # observation_space y en action_space
    state_space = 19.683 #env.observation_space.n
    print("There are ", state_space, " possible states")
    action_space = 9 #env.action_space.n
    print("There are ", action_space, " possible actions")

    
    Qtable_tictactoe = initialize_q_table(state_space, action_space)

    #TODO: Que luego de hacer un step, que el otro step lo haga la politica optima. 
    # Que juegue contra el algorimo del juego resuelto

    #TODO: Guardar la tabla en otro archivo para poder accederla

if __name__ == "__main__":
    main()
