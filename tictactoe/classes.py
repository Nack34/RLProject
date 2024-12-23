from error_classes import InvalidInputError, CellOccupiedError
import random

class Tablero():
    def __init__(self, img_x, img_o):
        self.tablero = [
            [0,0,0], 
            [0,0,0], 
            [0,0,0]
        ]
        self.img_x = img_x
        self.img_o = img_o


        #cuadros pintados
        self.cont = 0

    #mov vertical (sector arr,med,abj)
    def __get_fila(self,clic_y):
        fila = None
        if 35 <= clic_y <= 205:
            fila = 0
        elif 215 <= clic_y <= 385:
            fila = 1
        elif 395 <= clic_y <= 565:
            fila = 2

        return fila

    #mov horizontal (sector izq,med,der)
    def __get_columna(self,clic_x):
        col = None
        if 275 <= clic_x <= 445:
            col = 0
        elif 455 <= clic_x <= 625:
            col = 1
        elif 635 <= clic_x <= 805:
            col = 2
        
        return col


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

    def __get_libres(self):
        tablero = self.tablero
        libres = []
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == 0:
                     libres.append([i,j])

        return libres


    #return true if it finished, else false
    def marcar(self, turno, clic_x, clic_y, PANTALLA):
        tablero = self.tablero
        img_x = self.img_x
        img_o = self.img_o


        # depende cual cuadrado es, marco el punto del pos_x (300, 490, 670) izquierda a derecha, en aumento 180
        pos_col = 310 
        # depende cual cuadrado es, marco el punto del pos_y (80, 260, 440) arriba hacia abajo, en aumento 180
        pos_fil = 80

        columna = self.__get_columna(clic_x)
        fila = self.__get_fila(clic_y)

        # general checking
        if fila is None or columna is None:
            raise InvalidInputError("No le pegaste a nada, negro")
        
    
        if tablero[fila][columna] != 0:
            raise CellOccupiedError("Ya está ocupado, negro usurero")

        #updating internal structure
        tablero[fila][columna] = turno

        #start to updating screen to ther player
        icon_to_draw = img_x if turno == 1 else img_o


        pos_x_to_draw = pos_col + (180 * columna)
        pos_y_to_draw = pos_fil + (180 * fila)


        PANTALLA.blit(icon_to_draw, (pos_x_to_draw, pos_y_to_draw))


        #checking if game has all boxes marked
        cont = self.cont
        cont += 1
        if cont == 9:
            return True


        #checking if player has won
        if self.__check_player_win(turno):
            return True

        
        return False


    def marcar_aleatorio(self, turno, PANTALLA):
        tablero = self.tablero
        libres = self.__get_libres()
        
        img_x = self.img_x
        img_o = self.img_o


        # depende cual cuadrado es, marco el punto del pos_x (300, 490, 670) izquierda a derecha, en aumento 180
        pos_col = 310 
        # depende cual cuadrado es, marco el punto del pos_y (80, 260, 440) arriba hacia abajo, en aumento 180
        pos_fil = 80

        if len(libres) > 0:
            random_box = random.choice(libres)
            fila, columna = random_box
            tablero[fila][columna] = turno

            
            icon_to_draw = img_x if turno == 1 else img_o


            pos_x_to_draw = pos_col + (180 * columna)
            pos_y_to_draw = pos_fil + (180 * fila)


            PANTALLA.blit(icon_to_draw, (pos_x_to_draw, pos_y_to_draw))


            #checking if game has all boxes marked
            cont = self.cont
            cont += 1
            if cont == 9:
                return True


            #checking if player has won
            if self.__check_player_win(turno):
                return True

            
            return False
