import gymnasium as gym
from gymnasium import spaces
from error_classes import InvalidInputError, CellOccupiedError
import numpy as np

'''class Actions(Enum):
    LEFT_UP = 0
    LEFT_MIDDLE = 1
    LEFT_DOWN = 2
    MIDDLE_UP = 3
    MIDDLE_MIDDLE = 4
    MIDDLE_DOWN = 5
    RIGHT_UP = 6
    RIGHT_MIDDLE = 7
    RIGHT_DOWN = 8'''
    
class Tablero(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self):
        
        self.observation_space = spaces.Box(
            low=0,  # El valor mínimo que puede tener cada celda (0: vacío)
            high=2,  # El valor máximo que puede tener cada celda (2: O)
            shape=(3, 3),  # La forma de la matriz (3x3 para el tablero de ta-te-ti)
            dtype=np.int8  # El tipo de datos, ya que usamos enteros pequeños
        )



    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        
        #Initial state
        self.tablero = [
            [0,0,0], 
            [0,0,0], 
            [0,0,0]
        ]
        #cuadros pintados
        self.cont = 0

        self.turno_x = True

        return self.tablero, ""

    def __check_player_win(self, turno):
        tablero = self.tablero

        # Verificar filas
        for fila in range(3):
            if all(celda == turno for celda in tablero[fila]):
                return True

        # Verificar columnas
        for columna in range(3):
            if all(tablero[fila][columna] == turno for fila in range(3)):
                return True

        # Verificar diagonal principal
        if all(tablero[i][i] == turno for i in range(3)):
            return True

        # Verificar diagonal secundaria
        if all(tablero[i][2 - i] == turno for i in range(3)):
            return True

        # Si no hay ganador
        return False

    def action_space(self):
        tablero = self.tablero
        libres = []
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == 0:
                     libres.append([i,j])

        return libres


    def _get_recompensa():
        return 0
    
    def step(self, action):
        fila, columna = action 
        tablero = self.tablero
        turno = 1 if self.turno_x else 2

        # general checking
        if fila == -1 or columna == -1:
            raise InvalidInputError("No le pegaste a nada, negro")
        
    
        if tablero[fila][columna] != 0:
            raise CellOccupiedError("Ya está ocupado, negro usurero")

        #updating internal structure
        tablero[fila][columna] = turno

        # Cambia de X a O o de O a X
        self.turno_x = not self.turno_x 
  
        terminated = False
        #checking if game has all boxes marked
        self.cont += 1
        if self.cont == 9:
            terminated = True

        #checking if player has won
        if self.__check_player_win(turno):
            terminated = True
    
        reward = self._get_recompensa()
        return self.tablero, reward, terminated, False, ""
    
    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        pass # usar get_pos_pintar

    def get_pos_pintar(self, columna, fila):
        
        # depende cual cuadrado es, marco el punto del pos_x (300, 490, 670) izquierda a derecha, en aumento 180
        pos_col = 310 
        # depende cual cuadrado es, marco el punto del pos_y (80, 260, 440) arriba hacia abajo, en aumento 180
        pos_fil = 80


        pos_x_to_draw = pos_col + (180 * columna)
        pos_y_to_draw = pos_fil + (180 * fila)

        return (pos_x_to_draw, pos_y_to_draw)

