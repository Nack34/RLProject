import gymnasium as gym
from gymnasium import spaces
import numpy as np
import sys
import os
import pygame

# Agregar la carpeta padre al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from error_classes import InvalidInputError, CellOccupiedError
    
class Tablero(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array", "pygame"], "render_fps": 4}

    def config_pygame(self):
        # Pygame-specific attributes
        self.window_size = 1000
        self.cell_size = 180
        self.window = None
        self.clock = None
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

    def __init__(self, render_mode="human"):
        
        self.observation_space = spaces.Box(
            low=0,  # El valor mínimo que puede tener cada celda (0: vacío)
            high=2,  # El valor máximo que puede tener cada celda (2: O)
            shape=(3, 3),  # La forma de la matriz (3x3 para el tablero de ta-te-ti)
            dtype=np.int8  # El tipo de datos, ya que usamos enteros pequeños
        )
        self._penalizacion_por_tiempo = -1
        self.action_space = spaces.Tuple((spaces.Discrete(3), spaces.Discrete(3)))
        self.render_mode = render_mode
        self.config_pygame()

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        #Initial state
        self.tablero = np.zeros((3, 3), dtype=np.int8)
        self.tablero = np.zeros((3, 3), dtype=np.int8)
        self.turno_x = np.random.rand() < 0.1
        
        if not self.turno_x:
            i, j = np.random.randint(0, 3, size=2)
            self.tablero[i, j] = 1

        #cuadros pintados
        self.cont = 0

        self.terminated = False
        self.winner = None
        
        if self.render_mode == "pygame":
            self._pygame_init()

        return self.tablero, {"valid_actions": self.valid_actions()}

    def _pygame_init(self):
        if self.window is None:
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
            pygame.display.set_caption("Tic Tac Toe")
        
        if self.clock is None:
            self.clock = pygame.time.Clock()


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

    def valid_actions(self):
        tablero = self.tablero
        libres = []
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == 0:
                     libres.append([i,j])

        return libres
    
    def _get_game_terminated(self):
        turno = 1 if self.turno_x else 2

        terminated = False
        winner = None
        #checking if game has all boxes marked
        self.cont += 1
        if self.cont == 9:
            terminated = True
            winner=0

        #checking if player has won
        if self.__check_player_win(turno):
            terminated = True
            winner=turno

        return terminated, winner

    def _get_recompensa(self):
        return self._penalizacion_por_tiempo if self.winner is None else 5
    
    def step(self, action):
        info = {}
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
  
        terminated, info["winner"] = self._get_game_terminated()
        self.terminated = terminated
        self.winner = info["winner"]
    
        # Cambia de X a O o de O a X
        self.turno_x = not self.turno_x 

        reward = self._get_recompensa()
        info["valid_actions"] = self.valid_actions()
        return self.tablero, reward, terminated, False, info
    


    def render(self, mode=None):
        if mode is None:
            mode = self.render_mode

        if mode == "human":
            # Text-based rendering
            print("\n".join([" ".join([("." if cell == 0 else "X" if cell == 1 else "O") for cell in row]) for row in self.tablero]))
            print()

            if self.terminated:
                if not self.winner:
                    mensaje = "GAME TERMINATED: DRAW"
                else:
                    mensaje = f"GAME TERMINATED: WINNER {'X' if self.winner == 1 else 'O'}"

                largo = len(mensaje) + 2  # Contando los dos espacios adicionales para los guiones
                print(f"{'-' * (largo // 2)} {mensaje} {'-' * (largo // 2)}")
                print()


        
        elif mode == "pygame":
            if self.window is None:
                self._pygame_init()

            # Fill background
            self.window.fill(self.WHITE)

            # Draw grid lines
            for i in range(1, 3):
                # Vertical lines
                pygame.draw.line(
                    self.window,
                    self.BLACK,
                    (300 + i * self.cell_size, 80),
                    (300 + i * self.cell_size, 620),
                    4
                )
                # Horizontal lines
                pygame.draw.line(
                    self.window,
                    self.BLACK,
                    (300, 80 + i * self.cell_size),
                    (840, 80 + i * self.cell_size),
                    4
                )

            # Draw X's and O's
            for i in range(3):
                for j in range(3):
                    pos = self.get_pos_pintar(j, i)
                    if self.tablero[i][j] == 1:  # X
                        self._draw_x(pos)
                    elif self.tablero[i][j] == 2:  # O
                        self._draw_o(pos)

            pygame.display.flip()
            self.clock.tick(self.metadata["render_fps"])

    def _draw_x(self, pos):
        x, y = pos
        # Draw X with lines
        margin = 40
        pygame.draw.line(self.window, self.RED, 
                        (x - margin, y - margin),
                        (x + margin, y + margin), 8)
        pygame.draw.line(self.window, self.RED,
                        (x - margin, y + margin),
                        (x + margin, y - margin), 8)

    def _draw_o(self, pos):
        x, y = pos
        radius = 40
        pygame.draw.circle(self.window, self.BLUE, (x, y), radius, 8)

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
            self.window = None
            self.clock = None





















    '''def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()'''

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

