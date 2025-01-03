import pygame # type: ignore
from pygame.locals import * # type: ignore
from abc import ABC, abstractmethod #para clases abstractas
import random

from error_classes import InvalidInputError, CellOccupiedError
from constants import FPS, check_button, get_column, get_row




#board structure, only logic
class Tictactoe:
    def __init__(self):
        self.board = [[0] * 3 for _ in range(3)]
        self.moves = 0
    

    def get_libres(self):
        tablero = self.board
        libres = []
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == 0:
                    libres.append([i,j])

        return libres
    

    def __check_player_win(self, turno):
        tablero = self.board

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


    #return true if match ended, else false
    def mark(self, row, column, turn):
        tablero = self.board

        # general checking
        if row == -1 or column == -1:
            raise InvalidInputError("No le pegaste a nada, negro")
        
    
        if tablero[row][column] != 0:
            raise CellOccupiedError("Ya está ocupado, negro usurero")

        #updating internal structure
        tablero[row][column] = turn

  
        #checking if game has all boxes marked
        self.moves += 1

        if self.moves == 9:
            return True


        #checking if player has won
        if self.__check_player_win(turn):
            return True

        
        return False






class TictactoeManager(ABC):
    """Handles gameplay logic."""
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager

        self.running_main = True
        self.running_gameplay = True
        
        self.board = Tictactoe()
        self.turn = 1 #  1 = x, 2 = o
        self.ended_match = False

    @abstractmethod
    def _handle_game_event(self, event):
        pass

    @abstractmethod
    def _get_mode():
        pass

    def _reset(self):
        self.board = Tictactoe()
        self.turn = 1
        self.ended_match = False        

    def run(self):
        """Runs the gameplay loop."""
        self.screen_manager.start_match()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption(self._get_mode())
        while self.running_gameplay:

            mouse_pos = pygame.mouse.get_pos()
            self.screen_manager.update_dynamic(self.turn, mouse_pos)
            self.screen_manager.update_all_layers()

            for event in pygame.event.get():
                self._handle_game_event(event)

            pygame.display.update()
            self.screen_manager.clock.tick(FPS)

        pygame.mouse.set_visible(True)
        pygame.display.set_caption("Tictactoe")
        return self.running_main




class TictactoeManagerPVP(TictactoeManager):
    def _get_mode(self):
        return "PVP"

    def _handle_game_event(self, event):
        """Handles in-game events."""
        if event.type == pygame.QUIT:
            self.running_gameplay = False
            self.running_main = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if check_button(event,900,100): #reset
                self.screen_manager.start_match()
                self._reset()

            elif check_button(event,900,200): #back
                self.running_gameplay = False

            elif not self.ended_match:
                try:
                    clic_x, clic_y = event.pos

                    row = get_row(clic_y)
                    column = get_column(clic_x)

                    self.ended_match = self.board.mark(row, column, self.turn)

                    self.screen_manager.draw_symbol(row, column, self.turn)

                    
                    #changing turn
                    if not self.ended_match:
                        self.turn = 2 if self.turn == 1 else 1

                except (InvalidInputError, CellOccupiedError) as e:
                    print(e)



class TictactoeManagerPVB(TictactoeManager):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
    
        # crear evento manual
        self.EJECUTAR_FUNCION = pygame.USEREVENT + 1

        # Bandera para saber si el temporizador está activo
        self.temporizador_activo = False

    def _get_mode(self):
        return "PVB"


    def _handle_game_event(self, event):
        """Handles in-game events."""
        if event.type == pygame.QUIT:
            self.running_gameplay = False
            self.running_main = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not self.temporizador_activo:
            
            if check_button(event,900,100): #reset
                self.screen_manager.start_match()
                self._reset()

            elif check_button(event,900,200): #back
                self.running_gameplay = False

            elif not self.ended_match:
                try:
                    clic_x, clic_y = event.pos

                    row = get_row(clic_y)
                    column = get_column(clic_x)

                    self.ended_match = self.board.mark(row, column, self.turn)

                    self.screen_manager.draw_symbol(row, column, self.turn)

                    
                    #changing turn
                    if not self.ended_match:
                        self.turn = 2 if self.turn == 1 else 1
                        pygame.time.set_timer(self.EJECUTAR_FUNCION, 1000)  # Inicia el temporizador
                        self.temporizador_activo = True

                except (InvalidInputError, CellOccupiedError) as e:
                    print(e)
        
        elif  event.type == self.EJECUTAR_FUNCION and self.temporizador_activo:
                libres = self.board.get_libres()
                random_box = random.choice(libres)
                row, column = random_box

                # Ejecuta la función cuando se activa el temporizador (marcar aleatorio)
                self.ended_match = self.board.mark(row, column, self.turn)

                self.screen_manager.draw_symbol(row, column, self.turn)
                    
                # Detiene el temporizador
                pygame.time.set_timer(self.EJECUTAR_FUNCION, 0)
                self.temporizador_activo = False

                #changing turn
                if not self.ended_match:
                    self.turn = 2 if self.turn == 1 else 1