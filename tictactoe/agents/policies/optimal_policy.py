import numpy as np
from gymnasium.spaces import Box
import random
import numpy as np

class OptimalPolicy: # TODO: MODIFICAR ESTO USANDO DINAMIC PROGRAMING PARA que la funcion recursiva sea: value[state] = average de todas las acciones posibles(value[state+accion])
    class PlayerX:
        def __init__(self):
            self.id = 1
            self.oponent_id = 2

        def _oponente_coloco_en_centro(self, n_step, flattened):
            #print(f"coloco centro, n_step = {n_step}")
            if n_step == 1: # Marcar la esquina opuesta a la que marque antes
                if flattened[0] == 1:
                    return 8
                if flattened[2] == 1:
                    return 6
                if flattened[6] == 1:
                    return 2
                if flattened[8] == 1:
                    return 0
                
            return None            
                
        def _oponente_coloco_en_borde(self, n_step, flattened):
            #print(f"coloco borde, n_step = {n_step}")
            if n_step == 1: # Marcar la esquina que no es la opuesta a la que marque, y que en el siguiente paso puedo ganar
                if flattened[0] == 1:
                    if flattened[1] == 2: return 6
                    if flattened[3] == 2: return 2
                    return np.random.choice([2, 6])
                if flattened[2] == 1:
                    if flattened[1] == 2: return 8
                    if flattened[5] == 2: return 0
                    return np.random.choice([0, 8])
                if flattened[6] == 1:
                    if flattened[7] == 2: return 0
                    if flattened[3] == 2: return 8
                    return np.random.choice([0, 8])
                if flattened[8] == 1:
                    if flattened[7] == 2: return 2
                    if flattened[5] == 2: return 6
                    return np.random.choice([2, 6])
                
            elif n_step == 2: return 4 # Marcar el centro

            return None            

            
        def _oponente_coloco_en_esquina(self, n_step, flattened):
            #print(f"coloco esquina, n_step = {n_step}")
            if n_step == 1:
                if (flattened[0] and flattened[8]) or (flattened[2] and flattened[6]): # si marco en la opuesta, marco en el centro
                    return 4
                else: # si no marco en la opuesta, marco en la opuesta
                    if flattened[0] == 1:
                        return 8
                    if flattened[2] == 1:
                        return 6
                    if flattened[6] == 1:
                        return 2
                    if flattened[8] == 1:
                        return 0
            return None            
        
    class PlayerO:
        def __init__(self):
            self.id = 2
            self.oponent_id = 1

        def _oponente_coloco_en_centro(self, n_step, flattened):
            #print(f"coloco centro, n_step = {n_step}")
            if n_step == 1:
                return np.random.choice([0, 2, 6, 8])
                
            return None            
                
        def _oponente_coloco_en_borde(self, n_step, flattened):
            #print(f"coloco borde, n_step = {n_step}")
            if n_step == 1:
                return 4
            elif n_step == 2: 
                if (flattened[1] == 1 and flattened[7] == 1) or (flattened[3] == 1 and flattened[5] == 1):
                    return np.random.choice([0, 2, 6, 8])
                else:
                    if flattened[1] == 1 and flattened[3] == 1:
                        return 0
                    if flattened[1] == 1 and flattened[5] == 1:
                        return 2
                    if flattened[7] == 1 and flattened[3] == 1:
                        return 6
                    if flattened[7] == 1 and flattened[5] == 1:
                        return 8

            return None            
            
        def _oponente_coloco_en_esquina(self, n_step, flattened):
            #print(f"coloco esquina, n_step = {n_step}")
            if n_step == 1:
                return 4
                
            return None            

            
    def __init__(self, player = 1):
        self.reset(player=player)

    def reset(self, player = 1):
        self._player = self.PlayerX() if player == 1 else self.PlayerO() 
        self._internal_strategy = None
        self.initial_step=True
        self._n_step = 0
        print()
        print()
        print(f"Politica Optima: {"X" if self._player.id == 1 else "O"}")
        print()

    def step(self, state):
        if self.initial_step and self._player.id == 1: # Paso 0: Colocar X en una esquina
            self.initial_step=False
            return  np.random.choice([0, 2, 6, 8])

        self._n_step+=1
        
        flattened = state.flatten()
        if self._n_step == 1: # Paso 1: Elegir segun la mejor estrategia posible
            if flattened[4] == self._player.oponent_id: 
                self._internal_strategy = self._player._oponente_coloco_en_centro
            else: 
                self._internal_strategy = self._player._oponente_coloco_en_borde if flattened[1] == self._player.oponent_id or flattened[3] == self._player.oponent_id or flattened[5] == self._player.oponent_id or flattened[7] == self._player.oponent_id else self._player._oponente_coloco_en_esquina
            
            #print(self._player.id)
            #print(self._n_step)
            return self._internal_strategy(self._n_step, flattened)
        
        # Para cualquier otro _n_step que no es el 0 o el 1: 

        # Intentar ganar inmediatamente
        for i in range(9):
            if flattened[i] == 0:
                flattened[i] = self._player.id
                if check_win(flattened, self._player.id):
                    return i
                flattened[i] = 0
        
        # Bloquear al oponente si puede ganar
        for i in range(9):
            if flattened[i] == 0:
                flattened[i] = self._player.oponent_id
                if check_win(flattened, self._player.oponent_id):
                    return i
                flattened[i] = 0

        # Seguir la mejor estrategia posible
        posible_action = self._internal_strategy(self._n_step, flattened)
        if posible_action is not None:
            return posible_action
        
        # Colocar 'X' en cualquier posición disponible
        disponibles = []  # Lista para almacenar posiciones disponibles
        for i in range(9):
            if flattened[i] == 0:
                disponibles.append(i)  # Usar append para agregar elementos a la lista

        if disponibles:  # Si hay posiciones disponibles
            return np.random.choice(disponibles)  # Elegir una posición aleatoria
        else:
            return -1  # Retornar -1 si no hay posiciones disponibles
    
    def model_predict(self, model, state, valid_actions=None): # Metodo ADAPTER
        #print("self._player.id: ")
        #print(self._player.id)
        numero = self.step(state)
        fila = numero // 3
        columna = numero % 3

        action = [fila, columna]
        if action not in valid_actions:
            action = random.choice(valid_actions)
        return action

def check_win(flattened, player):
    """Verifica si el jugador dado ha ganado."""
    win_positions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
        [0, 4, 8], [2, 4, 6]              # Diagonales
    ]
    for pos in win_positions:
        if all(flattened[i] == player for i in pos):
            return True
    return False

# Ejemplo de uso:
def main():
    playerX = OptimalPolicy(player=1)
    playerO = OptimalPolicy(player=2)

    state = np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ], dtype=np.int8)
    player = 1
    step = playerX.step(state) if player == 1 else playerO.step(state)

    while step!=-1:
        print("Acción óptima:", step)
        
        # Marcar step en state
        row, col = divmod(step, 3)
        state[row, col] = player

        print("State:")
        print(state)

        player = 1 if player == 2 else 2
        step = playerX.step(state) if player == 1 else playerO.step(state)


if __name__ == "__main__":
    main()
