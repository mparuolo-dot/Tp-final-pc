import pygame
import random

paleta_colores = {
    "X" : (0,0,0),
    "." : (255,255,255),
    " " : (196, 181, 183),
    "G" : (105, 105, 105),        # seteamos la paleta de colores para cada signo
    "-" : (255, 255, 0),
    "o" : (255,255,255),
    "P" : (196, 181, 183),
    "T" : (105, 105,105)
}

largo_fila = 28
alto_mapa = 31      # seteamos los parametros del mapa y agregados y el tamaño de los pixeles
tamaño_pixel = 20
tamaño_score = 60


class Mapa:
    """
    clase para el mapa del juego que maneja la matriz y sus tiles
    """
    def __init__(self, archivo_mapa):
        self.archivo = archivo_mapa
        self.grilla = []  # aca guardamos las lineas en forma de matriz
        self.comida_faltante = 0
        self.poscion_x_pacman = 0
        self.poscion_y_pacman = 0
        self.cargar_mapa()

    def cargar_mapa(self):
        """
        Funcion para cargar, verificar y validar el archivo de texto del mapa
        """
        ghost_house = False
        hay_pacman = False
        try:
            with open(self.archivo, "r") as f:  # abrimos el archivo de texto con el mapa
                for linea in f:
                    self.grilla.append(list(linea.strip()))  # guardamos cada linea en una lista
                if len(self.grilla) != alto_mapa:  # si el tamaño de la fila es diferente al establecido
                    raise ValueError("El alto del mapa es incorrecto")
                for fila in range(alto_mapa):
                    if len(self.grilla[fila]) != largo_fila:  # si el largo es incorrecto
                        raise ValueError("El largo del mapa es incorrecto")
                    for columna in range(largo_fila):
                        if self.grilla[fila][columna] not in paleta_colores.keys():  # si el caracter no es reconocido
                            raise ValueError(f"El caracter {self.grilla[fila][columna]} es desconocido")
                        if self.grilla[fila][columna] == "G":  # verificamos si existe Ghost house
                            ghost_house = True
                        if self.grilla[fila][columna] == "P":  # verificamos si existe Pacman
                            hay_pacman = True
                if ghost_house == False:
                    raise ValueError("No hay ghost house")
                if hay_pacman == False:
                    raise ValueError("No hay pacman")

        except FileNotFoundError:
            raise FileNotFoundError("No se encontro el archivo")

        for fila in range(alto_mapa):
            for columna in range(largo_fila):  # buscamos las posiciones iniciales y la comida
                if self.grilla[fila][columna] == "P":
                    self.poscion_x_pacman = columna
                    self.poscion_y_pacman = fila
                elif self.grilla[fila][columna] == "." or self.grilla[fila][columna] == "o":
                    self.comida_faltante += 1

    def es_libre(self, fila, columna) -> bool:
        """
        Funcion para verificar si el tile es un espacio por el que se puede transitar de forma estandar
        """
        tile = self.grilla[fila][columna % largo_fila]
        if tile != "X" and tile != "G" and tile != "-":
            return True
        return False

    def es_libre_casa(self, fila, columna) -> bool:
        """
        Funcion para verificar si el tile es libre para los ojos de fantasmas volviendo a casa
        """
        tile = self.grilla[fila][columna % largo_fila]
        if tile != "X":
            return True
        return False

    def es_ghost_house(self, fila, columna) -> bool:
        """
        Funcion para verificar si un tile pertenece a la casa de los fantasmas
        """
        tile = self.grilla[fila][columna % largo_fila]
        if tile == "G" or tile == "-":
            return True
        return False

    def es_tunnel(self, fila, columna) -> bool:
        """
        Funcion para verificar si un tile es el tunel de teletransporte
        """
        tile = self.grilla[fila][columna % largo_fila]
        if tile == "T":
            return True
        return False

    def dibujar(self, pantalla):
        """
        Funcion para dibujar todos los tiles del mapa en pantalla
        """
        for fila in range(alto_mapa):
            for columna in range(largo_fila):
                color = paleta_colores[self.grilla[fila][columna]]  # obtenemos el color de cada posicion
                lugar = (columna * tamaño_pixel, fila * tamaño_pixel + tamaño_score - 10, tamaño_pixel, tamaño_pixel)
                centro_x = columna * tamaño_pixel + tamaño_pixel // 2
                centro_y = fila * tamaño_pixel + tamaño_pixel // 2 + tamaño_score - 10
                centro_pixel = (centro_x, centro_y)
                if self.grilla[fila][columna] == ".":  # si el tile es comida chica
                    pygame.draw.rect(pantalla, (196, 181, 183), lugar)
                    pygame.draw.circle(pantalla, color, centro_pixel, 2)
                elif self.grilla[fila][columna] == "o":  # si el tile es comida grande
                    pygame.draw.rect(pantalla, (196, 181, 183), lugar)
                    pygame.draw.circle(pantalla, color, centro_pixel, 4)
                else:
                    pygame.draw.rect(pantalla, color, lugar)


class Personajes:   
    """
    clase para los personajes del juego
    
    Args:
        mapa (list): mapa del juego
    """
    def __init__(self,mapa,pantalla):
        self.mapa = mapa.grilla  
        self.pantalla = pantalla


class Pacman(Personajes): 
    """
    clase para el pacman 
    
    Args:
        Personajes (class): clase para los personajes del juego
    """
    def __init__(self,x: int,y: int , mapa, pantalla):
        """   
        Args:
            x (int): posicion x del pacman en tiles
            y (int): posicion y del pacman en tiles
        """
        Personajes.__init__(self, mapa , pantalla)
        self.x = x * tamaño_pixel   # seteamos la posicion de pacman en pixeles cuando x e y los teniamos en tiles del mapa
        self.y = y * tamaño_pixel    
        self.power_pellet = False  #seteamos el valor de power_pellet 
        self.tiempo_de_power_pellet = 0 # seteamos el tiempo de duracion del power_pellet
        self.direccion = ""  # seteamos la direccion de pacman para usar en mover
        self.proxima_direccion = ""  # seteamos la proxima direccion de pacman para usar en mover
        self.pacman_boca_cerrada = pygame.transform.scale(pygame.image.load("boca_cerrada.png"), (tamaño_pixel, tamaño_pixel))
        self.pacman_boca_abierta = pygame.transform.scale(pygame.image.load("boca_abierta.png"), (tamaño_pixel, tamaño_pixel))
        self.pacman_boca_cerrada_parcial = pygame.transform.scale(pygame.image.load("boca_semiabierta.png"), (tamaño_pixel, tamaño_pixel))
        self.contador_fps_dibujo = 0
        self.mostrar_pacman = self.pacman_boca_abierta
        self.direccion_para_imagen= "derecha"
        self.rotacion = 0
    
    def mover(self,velocidad :int, dt : int):
        """
        Funcion para mover el pacman en la pantalla
        
        Args:
            velocidad (int): velocidad del pacman
        """
        claves = pygame.key.get_pressed()    # obtenemos las teclas presionadas         
        velocidad_tiles = 1 # seteamos la velocidad de pacman en tiles diferenciada de la velocidad en pixeles
        velocidad_pixeles = velocidad * 60
        if claves[pygame.K_LEFT]:
            self.proxima_direccion = "izquierda" 
        elif claves[pygame.K_RIGHT]:
            self.proxima_direccion = "derecha" 
        elif claves[pygame.K_UP]:                       # Guardamos la proxima direccion de pacman en base al input de las teclas
            self.proxima_direccion = "arriba"
        elif claves[pygame.K_DOWN]:
            self.proxima_direccion = "abajo"
        if self.x % tamaño_pixel < velocidad_pixeles * dt and self.y % tamaño_pixel < velocidad_pixeles * dt:    # verificamos si el pacman esta cerca del centro de un tile dependiendo de la velocidad
            self.x = int(self.x // tamaño_pixel) * tamaño_pixel
            self.y = int(self.y // tamaño_pixel) * tamaño_pixel  #sacamos decimales y lo multiplicamos por el tamaño de los pixeles para qeu no se superponga con paredes
            proxima_doblar_x = self.x // tamaño_pixel
            proxima_doblar_y = self.y // tamaño_pixel  # para verificar las paredes y a donde tenemos que ir volvemos a pasar de pixeles a tiles

            if self.proxima_direccion == "izquierda":
                proxima_doblar_x -= velocidad_tiles
                self.direccion_para_imagen = "izquierda"
            elif self.proxima_direccion == "derecha":
                proxima_doblar_x += velocidad_tiles
                self.direccion_para_imagen = "derecha"
            elif self.proxima_direccion == "arriba":   # dependiendo la direccion restamos o sumamos la velocidad de tiles a la proxima direccion
                proxima_doblar_y -= velocidad_tiles
                self.direccion_para_imagen = "arriba"
            elif self.proxima_direccion == "abajo":
                proxima_doblar_y += velocidad_tiles
                self.direccion_para_imagen = "abajo"



            if self.mapa[proxima_doblar_y ][proxima_doblar_x % largo_fila] != "X" :  # verificamos si la proxima posicion a doblar es una pared y si no es guardamos la direccion
                self.direccion = self.proxima_direccion

            #la parte anteriror la usamos para verificar si podiamos doblar o no y la parte siguiente si no podemos doblar la usamos para ver si podemos avanzar en la direccion guardada

            proximo_bloque_adelante_x = self.x // tamaño_pixel
            proximo_bloque_adelante_y = self.y // tamaño_pixel  # para verificar las paredes y a donde tenemos que ir volvemos a pasar de pixeles a tiles

            if self.direccion == "izquierda":
                proximo_bloque_adelante_x -= velocidad_tiles
                self.direccion_para_imagen = "izquierda"
            elif self.direccion == "derecha":
                proximo_bloque_adelante_x += velocidad_tiles
                self.direccion_para_imagen = "derecha"
            elif self.direccion == "arriba":                        # dependiendo la direccion restamos o summamos la velocidad de tiles a la proxima direccion
                proximo_bloque_adelante_y -= velocidad_tiles
                self.direccion_para_imagen = "arriba"
            elif self.direccion == "abajo":
                proximo_bloque_adelante_y += velocidad_tiles
                self.direccion_para_imagen = "abajo"



            if self.mapa[proximo_bloque_adelante_y][proximo_bloque_adelante_x % largo_fila] == "X" : # vemos si el bloque al que avanzamos es una pared si es guarsdamops una direciion vacia para no movernos  usamos % largo_fila para que no se salga del mapa
                self.direccion = ""

        if self.direccion == "izquierda":
            self.x -= velocidad_pixeles * dt
        elif self.direccion == "derecha":
            self.x += velocidad_pixeles * dt
        elif self.direccion == "arriba":            # dependiendo la direccion restamos o summamos la velocidad en pixeles que es lo que mopstramos en pantalla
            self.y -= velocidad_pixeles * dt   
        elif self.direccion == "abajo":
            self.y += velocidad_pixeles * dt

        if self.x < 0:                            # si llegamos al tunel por la izquierda
            self.x = (largo_fila - 1) * tamaño_pixel  #seteamos posicion al tunel de la derecha
        elif self.x > (largo_fila - 1) * tamaño_pixel:   # si llegamos al tunel por derecha
            self.x = 0  #seteamos posicion al tunel de la izquierda

    
    def comer(self, fantasmas_activos=[]) -> int: 
        """
        Funcion para comer comida y devolver el valor de la comida
        
        Returns:
            int: valor de la comida
        """
        if self.x % tamaño_pixel < 4 and self.y % tamaño_pixel < 4:    # verificamos si el pacman esta cerca del centro el tile en pixeles para qeu pueda comer en base a veloidades
            fila = int(self.y // tamaño_pixel)
            columna = int(self.x // tamaño_pixel)  # para verificar las comida pasamos de pixeles a tiles
            if self.mapa[fila][columna] == ".": # verificamos si el tile es comida chica
                self.mapa[fila][columna] = " "  # seteamos el tile vacio
                return 10  # devolvemos el valor de la comida
            
            elif self.mapa[fila][columna] == "o":  # verificamos si el tile es comida grande      
                self.mapa[fila][columna] = " "  # seteamos el tile vacio
                self.power_pellet = True  # seteamos el power_pellet a true 
                self.tiempo_de_power_pellet = 360  # seteamos el tiempo de duracion del power_pellet en frames 60*6
                for fantasma in fantasmas_activos:  # asustamos a todos los fantasmas cargados en el juego
                    fantasma.asustado()
                return 50  # devolvemos el valor de la comida
            
    def ver_power_pellet(self) -> bool:
        """
        Funcion para verificar si el power_pellet esta activo
        
        Returns:
            bool: si el power_pellet esta activo o no
        """
        if self.tiempo_de_power_pellet > 0:  # verificamos si el power_pellet esta activo
            self.tiempo_de_power_pellet -= 1  # restamos 1 a la duracion del power_pellet por cada frame
            if self.tiempo_de_power_pellet == 0:  # verificamos si el power_pellet termino
                self.power_pellet = False  # seteamos el power_pellet a false
                return self.power_pellet  # devolvemos el power_pellet = False
            else:  # si el power_pellet no termino
                self.power_pellet = True  # lo dejamos en true al power_pellet
                return self.power_pellet  # devolvemos el power_pellet = True
        else:
            self.power_pellet = False 
            return self.power_pellet 
        
    def dibujar(self,dt):
        """
        Funcion para dibujar el pacman en la pantalla
        """
        self.contador_fps_dibujo +=  1 #sumamos uno por cada fps
        if self.contador_fps_dibujo == 0: 
            self.mostrar_pacman = self.pacman_boca_abierta
        elif self.contador_fps_dibujo == 20 : 
            self.mostrar_pacman = self.pacman_boca_cerrada_parcial
        elif self.contador_fps_dibujo == 40 : 
            self.mostrar_pacman = self.pacman_boca_cerrada
            self.contador_fps_dibujo = 0
        


        if self.direccion_para_imagen == "arriba":
            self.rotacion = 90
            self.pantalla.blit(pygame.transform.rotate(self.mostrar_pacman,self.rotacion), (int(self.x) , int(self.y) + tamaño_score -10 ))
        elif self.direccion_para_imagen == "izquierda":
            self.pantalla.blit(pygame.transform.flip(self.mostrar_pacman,True,False ), (int(self.x) , int(self.y) + tamaño_score -10 ))
        elif self.direccion_para_imagen == "abajo":
            self.rotacion = 270
            self.pantalla.blit(pygame.transform.rotate(self.mostrar_pacman,self.rotacion), (int(self.x) , int(self.y) + tamaño_score -10 ))
        else:
            self.pantalla.blit(self.mostrar_pacman, (int(self.x) , int(self.y) + tamaño_score -10  ))
    def animacion_muerte(self):
        for i in range(1,11):
            muerte_imagen = pygame.transform.scale(pygame.image.load(f"muerte_{i}.png"), (tamaño_pixel, tamaño_pixel))
            pygame.draw.rect(self.pantalla, (196, 181, 183), (int(self.x), int(self.y) + tamaño_score - 10, tamaño_pixel, tamaño_pixel))
            self.pantalla.blit(muerte_imagen, (int(self.x), int(self.y) + tamaño_score - 10))
            pygame.display.flip()
            pygame.time.delay(120)

            



class Fantasma(Personajes):
    """
    clase base para los fantasmas del juego que se mueven por pixeles como Pac-Man
    """
    def __init__(self, mapa, x_inicial, y_inicial, esquina,pantalla):
        Personajes.__init__(self, mapa, pantalla)
        self.x_inicial = x_inicial * tamaño_pixel
        self.y_inicial = y_inicial * tamaño_pixel
        self.mapa = mapa
        self.x = x_inicial * tamaño_pixel
        self.y = y_inicial * tamaño_pixel
        self.direccion = "arriba"  # direccion inicial para salir de la casa
        self.proxima_direccion = ""
        self.velocidad = 1.5  # velocidad equivalente a la de Pac-Man (normal 1.5)
        self.salio = False
        self.color = (0, 0, 0)
        self.esta_asustado = False
        self.tiempo_asustado = 0
        self.duracion_asustado = 360 # 6 segundos en frames (60*6)
        self.esquina = esquina  # tupla (fila, columna) asignada para scatter
        self.modo = 'scatter'
        self.ojos = False
        self.ojos_imagen = pygame.transform.scale(pygame.image.load("ojos.png"), (tamaño_pixel, tamaño_pixel))
        self.asustado_imagen = pygame.transform.scale(pygame.image.load("asustado.png"), (tamaño_pixel, tamaño_pixel))
        self.asustado_imagen_blanco = pygame.transform.scale(pygame.image.load("asustado_blanco.png"), (tamaño_pixel, tamaño_pixel))
        self.orden_salida = 0
            

    def dibujar(self, pantalla):
        """
        Funcion para dibujar al fantasma en pantalla usando sus sprites
        """
        pos_y_pantalla = int(self.y) + tamaño_score - 10
        pos_x_pantalla = int(self.x) 

        if self.ojos == True:
            pantalla.blit(self.ojos_imagen, (pos_x_pantalla, pos_y_pantalla))
        elif self.esta_asustado == True:
            if self.tiempo_asustado < 120 :
                if (int(self.tiempo_asustado // 15)) % 2 == 0:
                    pantalla.blit(self.asustado_imagen_blanco, (pos_x_pantalla, pos_y_pantalla))
                else:
                    pantalla.blit(self.asustado_imagen, (pos_x_pantalla, pos_y_pantalla))
            else:
                pantalla.blit(self.asustado_imagen, (pos_x_pantalla, pos_y_pantalla))

        else:
            pantalla.blit(self.imagen_fantasmas, (pos_x_pantalla, pos_y_pantalla))


    def mover(self, fila, columna, proxima_direccion, dt, puntos_comidos):
        """
        Funcion para mover el fantasma píxel por píxel calculando intersecciones como Pac-Man
        """
        # Seteamos la velocidad dependiendo de los estados
        velocidad = 1.5
        if self.ojos == True:
            velocidad = 3.0  # Los ojos vuelan rapido a casa
        elif self.esta_asustado == True:
            velocidad = 0.9  # Asustado reduce velocidad
        elif self.mapa.es_tunnel(int(self.y // tamaño_pixel), int(self.x // tamaño_pixel)) == True:
            velocidad = 0.8  # El tunel los frena

        velocidad_pixeles = velocidad * 60

        if self.esta_asustado == True:
            self.tiempo_asustado -= 60 * dt  # Decrementamos los frames del temporizador asustado
            if self.tiempo_asustado <= 0:
                self.esta_asustado = False
                self.tiempo_asustado = 0

        if self.salio == False:
            puede_salir = False
            if self.orden_salida == 0:
                puede_salir = True
            elif self.orden_salida == 1 and puntos_comidos >= 30:
                puede_salir = True
            elif self.orden_salida == 2 and puntos_comidos >= 60:
                puede_salir = True
            elif self.orden_salida == 3 and puntos_comidos >= 90:
                puede_salir = True
            if puede_salir == True:
                self.direccion = "arriba"
                self.y -= velocidad_pixeles * dt
                fila_actual = int(self.y // tamaño_pixel)
                columna_actual = int(self.x // tamaño_pixel)
                if self.mapa.es_ghost_house(fila_actual, columna_actual) == False:
                    self.salio = True
            return

        # Si el fantasma regresa a casa siendo ojos y llega al origen
        if self.ojos == True:
            if self.mapa.es_ghost_house(int(self.y // tamaño_pixel), int(self.x // tamaño_pixel)) == True:
                self.x = self.x_inicial
                self.y = self.y_inicial
                self.ojos = False
                self.salio = False # Vuelve a regenerarse dentro y sale de forma normal
                return

        # Verificamos si esta centrado en una baldosa para calcular la proxima direccion
        if self.x % tamaño_pixel < velocidad_pixeles * dt and self.y % tamaño_pixel < velocidad_pixeles * dt:
            self.x = int(self.x // tamaño_pixel) * tamaño_pixel
            self.y = int(self.y // tamaño_pixel) * tamaño_pixel

            posicion_x = int(self.x // tamaño_pixel)
            posicion_y = int(self.y // tamaño_pixel)

            posicion_target_fila, posicion_target_columna = self.target(fila, columna, proxima_direccion)
            if self.modo == 'scatter':
                posicion_target_fila, posicion_target_columna = self.esquina[0], self.esquina[1]
            if self.ojos == True:
                posicion_target_fila, posicion_target_columna = int(self.y_inicial // tamaño_pixel), int(self.x_inicial // tamaño_pixel)

            # Direcciones posibles en formato (nombre, dx, dy, opuesta)
            direcciones_giro = [
                ("arriba", 0, "abajo", -1),
                ("abajo", 0, "arriba", 1),
                ("izquierda", -1,"derecha", 0),
                ("derecha", 1, "izquierda", 0),
            ]

            direciones_posibles = []
            for direccion, movimiento_x, direccion_opuesta, movimiento_y in direcciones_giro:
                if self.direccion != direccion_opuesta:  # Los fantasmas no pueden regresar sobre sus pasos
                    proxima_columna = posicion_x + movimiento_x
                    proxima_fila = posicion_y + movimiento_y
                    
                    if  proxima_fila < alto_mapa  and proxima_columna < largo_fila:
                        if self.ojos == True:
                            puede_moverse = self.mapa.es_libre_casa(proxima_fila, proxima_columna)
                        else:
                            puede_moverse = self.mapa.es_libre(proxima_fila, proxima_columna)

                        if puede_moverse == True:
                            # Calculamos distancia euclidiana de baldosas al objetivo
                            distancia = ((posicion_target_fila - proxima_fila) ** 2 + (posicion_target_columna - proxima_columna) ** 2) ** 0.5
                            direciones_posibles.append((direccion, distancia))

            if len(direciones_posibles) > 0:
                if self.esta_asustado == True:
                    # Elige de manera aleatoria al estar asustado
                    elegida = random.choice(direciones_posibles)
                    self.proxima_direccion = elegida[0]
                else:
                # Buscamos manualmente la direccion con la menor distancia
                    menor_distancia = 100000.0  # Seteamos un valor inicial muy alto
                    direccion_final = self.direccion  # Por defecto mantenemos la actual
                    
                    for direccion, distancia in direciones_posibles:
                        if distancia < menor_distancia:
                            menor_distancia = distancia
                            direccion_final = direccion
                    
                    self.proxima_direccion = direccion_final

                self.direccion = self.proxima_direccion
            

        # Aplicamos movimiento en pixeles
        if self.direccion == "izquierda":
            self.x -= velocidad_pixeles * dt
        elif self.direccion == "derecha":
            self.x += velocidad_pixeles * dt
        elif self.direccion == "arriba":
            self.y -= velocidad_pixeles * dt
        elif self.direccion == "abajo":
            self.y += velocidad_pixeles * dt

        # Control del tunel de teletransporte lateral
        if self.x < 0:
            self.x = (largo_fila - 1) * tamaño_pixel
        elif self.x > (largo_fila - 1) * tamaño_pixel:
            self.x = 0

    def asustado(self):
        """
        Funcion para alertar al fantasma de que Pacman comio un power pellet
        """
        self.esta_asustado = True
        self.tiempo_asustado = 360  # 6 segundos en frames (60*6)
        
        # Invertimos la direccion de forma automatica
        if self.direccion == "izquierda":
            self.direccion = "derecha"
        elif self.direccion == "derecha": 
            self.direccion = "izquierda"
        elif self.direccion == "arriba": 
            self.direccion = "abajo"
        elif self.direccion == "abajo": 
            self.direccion = "arriba"
    


class Blinky(Fantasma):
    """
    clase para Blinky (Rojo - El perseguidor)
    """
    def __init__(self, mapa, x_inicial, y_inicial, esquina,pantalla):
        Fantasma.__init__(self, mapa, x_inicial, y_inicial, esquina,pantalla)
        self.imagen_fantasmas = pygame.transform.scale(pygame.image.load("blinky.png"), (tamaño_pixel, tamaño_pixel))

    def target(self, pacman_fila, pacman_columna, proxima_direccion):
        return pacman_fila, pacman_columna


class Pinky(Fantasma):
    """
    clase para Pinky (Rosa - El emboscador)
    """
    def __init__(self, mapa, x_inicial, y_inicial, esquina,pantalla):
        Fantasma.__init__(self, mapa, x_inicial, y_inicial, esquina,pantalla)
        self.imagen_fantasmas = pygame.transform.scale(pygame.image.load("pinky.png"), (tamaño_pixel, tamaño_pixel))


    def target(self, pacman_fila, pacman_columna, proxima_direccion):
        target_fila = 0
        target_columna = 0
        if proxima_direccion == "arriba":
            target_fila = -4
        elif proxima_direccion == "abajo":
            target_fila = 4
        elif proxima_direccion == "izquierda":
            target_columna = -4
        elif proxima_direccion == "derecha":
            target_columna = 4
        return pacman_fila + target_fila, pacman_columna + target_columna


class Inky(Fantasma):
    """
    clase para Inky (Celeste - El flanqueador)
    """
    def __init__(self, mapa, x_inicial, y_inicial, esquina,pantalla, blinky=None):
        Fantasma.__init__(self, mapa, x_inicial, y_inicial, esquina,pantalla)
        self.blinky = blinky
        self.imagen_fantasmas = pygame.transform.scale(pygame.image.load("inky.png"), (tamaño_pixel, tamaño_pixel))

    def target(self, pacman_fila, pacman_columna, proxima_direccion):
        target_fila = 0
        target_columna = 0
        if proxima_direccion == "arriba":
            target_fila = -2
        elif proxima_direccion == "abajo":
            target_fila = 2
        elif proxima_direccion == "izquierda":
            target_columna = -2
        elif proxima_direccion == "derecha":
            target_columna = 2
        
        celda_intermedia_fila = pacman_fila + target_fila    
        celda_intermedia_columna = pacman_columna + target_columna

        if self.blinky is not None:
            blinky_fila = int(self.blinky.y // tamaño_pixel)
            blinky_columna = int(self.blinky.x // tamaño_pixel)
            vector_fila = celda_intermedia_fila - blinky_fila
            vector_columna = celda_intermedia_columna - blinky_columna
            return celda_intermedia_fila + vector_fila, celda_intermedia_columna + vector_columna
        else:
            return pacman_fila, pacman_columna


class Clyde(Fantasma):
    """
    clase para Clyde (Naranja - El timido)
    """
    def __init__(self, mapa, x_inicial, y_inicial, esquina,pantalla):
        Fantasma.__init__(self, mapa, x_inicial, y_inicial, esquina,pantalla)
        self.imagen_fantasmas = pygame.transform.scale(pygame.image.load("clyde.png"), (tamaño_pixel, tamaño_pixel))

    def target(self, pacman_fila, pacman_columna, proxima_direccion):
        ghost_fila = int(self.y // tamaño_pixel)
        ghost_columna = int(self.x // tamaño_pixel)
        distancia = ((pacman_fila - ghost_fila) ** 2 + (pacman_columna - ghost_columna) ** 2) ** 0.5
        if distancia > 8:
            return pacman_fila, pacman_columna
        else:
            return self.esquina[0], self.esquina[1]


class Spike(Fantasma):
    """
    clase para Spike (Verde - El interceptor)
    """
    def __init__(self, mapa, x_inicial, y_inicial, esquina,pantalla):
        Fantasma.__init__(self, mapa, x_inicial, y_inicial, esquina,pantalla)
        self.imagen_fantasmas = pygame.transform.scale(pygame.image.load("spike.png"), (tamaño_pixel, tamaño_pixel))

    def target(self, pacman_fila, pacman_columna, proxima_direccion):
        target_fila = 0
        target_columna = 0
        if proxima_direccion == "arriba":
            target_fila -= 3
        elif proxima_direccion == "abajo":
            target_fila -= 3
        elif proxima_direccion == "izquierda":
            target_columna = -3
        elif proxima_direccion == "derecha":
            target_columna -= 3
        return pacman_fila + target_fila, pacman_columna + target_columna




class Coward(Fantasma):
    """
    clase para Coward (Violeta - El cobarde)
    """
    def __init__(self, mapa, x_inicial, y_inicial, esquina,pantalla):
        Fantasma.__init__(self, mapa, x_inicial, y_inicial, esquina,pantalla)
        self.imagen_fantasmas = pygame.transform.scale(pygame.image.load("coward.png"), (tamaño_pixel, tamaño_pixel))


    def target(self, pacman_fila, pacman_columna, prox_direccion):
        ghost_fila = int(self.y // tamaño_pixel)
        ghost_columna = int(self.x // tamaño_pixel)
        distancia = ((pacman_fila - ghost_fila) ** 2 + (pacman_columna - ghost_columna) ** 2) ** 0.5
        if distancia > 5:
            return pacman_fila, pacman_columna
        else:
            return self.esquina[0], self.esquina[1]


class Puntaje:
    def __init__(self, score: int, pantalla):
        """
        Args:
            score (int): puntaje del juego
        """
        self.pantalla = pantalla
        self.puntos = score #seteamos el puntaje
        self.high_score =  self.cargar_high_score() # cargamos el puntaje maximo
        self.vidas = 3 # seteamos las vidas
        self.lvl = 1 # seteamos el nivel
        self.vida_extra_otorgada = False # controlamos la vida extra para que se otorgue una sola vez

    def cargar_high_score(self) -> int: 
        """
        Funcion para cargar el puntaje maximo
        
        Returns:
            int: puntaje maximo
        """
        try:
            with open("high_score.txt", "r") as f:
                high_score = int(f.read()) # gyuardamos el puntaje maximo
                return high_score
        except FileNotFoundError: # si no existe el archivo
            high_score = 0  # seteamos el puntaje maximo en 0
            return high_score

    def actualizar_high_score(self):
        """
        Funcion para actualizar el puntaje maximo
        """
        with open("high_score.txt", "w") as f:
            f.write(str(self.puntos))
        

    def actualizar_puntaje(self, score: int):
        """
        Funcion para actualizar el puntaje
        
        Args:
            score (int): puntaje del juego
        
        Returns:
            int: puntaje actualizado
        """
        self.puntos += score # sumamos el puntaje al puntaje inicial
        if self.puntos > self.high_score: # si el puntaje actual es mayor al puntaje maximo
            self.high_score = self.puntos # seteamos el puntaje maximo al puntaje actual
        
        if self.puntos >= 10000 and self.vida_extra_otorgada == False: # otorgamos vida extra al llegar a 10.000 puntos
            self.vidas += 1
            self.vida_extra_otorgada = True
            
        return self.puntos # devolvemos el puntaje actualizado

    def actualizar_lvl(self, lvl: int):
        """
        Funcion para actualizar el nivel
        
        Args:
            lvl (int): nivel del juego
        """
        self.lvl += lvl # seteamos el nivel

    def mostrar(self):
        """
        Funcion para mostrar el puntaje en la pantalla
        
        """
        fuente = pygame.font.SysFont("Courier", 40)  # seteamos la fuente para el txto
        fuente_lvl = pygame.font.SysFont("Courier", 20)
        texto_score = fuente.render(f"{self.puntos}", True, (255, 255, 255)) # guardmaos los puntos
        texto_high_score_texto = fuente.render("HIGH SCORE", True, (255, 255, 255)) # guardamos el mensaje high score
        texto_high_score = fuente.render(f"{self.high_score}", True, (255, 255, 255)) # guradmaos el puntaje maximo
        texto_lvl = fuente_lvl.render(f"LVL {self.lvl}", True, (255, 255, 255)) # guardamos el nivel
        self.pantalla.blit(texto_score, (30,30)) # mostramos los ountois en la pantalla
        self.pantalla.blit(texto_high_score_texto, (175,0)) # mostramos el mensaje highscore
        self.pantalla.blit(texto_high_score, (175,30)) # mostramos el puntaje maximo
        self.pantalla.blit(texto_lvl, (450,40)) # mostramos el nivel

        if self.vidas <= 0: # si no quedan vidas
            self.pantalla.fill((0,0,0))
            fuente = pygame.font.SysFont("Courier", 60)  # seteamos la fuente para el txto
            texto_game_over = fuente.render("GAME OVER", True, (255, 255, 255)) # guardamos el mensaje game over
            self.pantalla.blit(texto_game_over, (120,275)) # mostramos el mensaje game over
        elif self.vidas == 1: # si quedan 1 vidas
            pygame.draw.circle(self.pantalla,(255, 217, 0), (50, 675), 10) # dibujamos las vidas en la pantalla
        elif self.vidas == 2: # si quedan 2 vidas
            pygame.draw.circle(self.pantalla,(255, 217, 0), (50, 675), 10) # dibujamos las vidas en la pantalla
            pygame.draw.circle(self.pantalla,(255, 217, 0), (80, 675), 10)
        elif self.vidas >= 3: # si quedan 3 o mas vidas
            pygame.draw.circle(self.pantalla,(255, 217, 0), (50, 675), 10)
            pygame.draw.circle(self.pantalla,(255, 217, 0), (80, 675), 10)   # dibujamos las vidas en la pantalla
            pygame.draw.circle(self.pantalla,(255, 217, 0), (110, 675), 10)
        

class Juego:
    def __init__(self):
        """
        Funcion para iniciar el juego
        """
        pygame.init()  # inicializamos la pantalla del pygame
        pygame.mixer.init()
        pygame.mixer.music.load("musica_inicio.mp3")
        self.sonido_muerte = pygame.mixer.Sound("muerte.mp3")
        self.sonido_comida = pygame.mixer.Sound("pacman_come.mp3")
        self.sonido_comer_fantasma = pygame.mixer.Sound("pacman_come_fantasma.mp3")
        pygame.mixer.music.play(-1)
        self.pantalla = pygame.display.set_mode((largo_fila * tamaño_pixel, (alto_mapa * tamaño_pixel) + tamaño_score + 30))  # creamse la pantalla del juego
        self.fps =  pygame.time.Clock() # creamos un objeto que usamos para los fps
        self.puntaje = Puntaje(0, self.pantalla) # creamos un objeto de la clase Puntaje y lo seteamos para que empeize en 0 
        self.estado = "Inicio"
        self.mostrar_enter = True
        self.fps_por_texto_enter = 0
        self.fantasmas = [
                {"nombre": "Blinky" ,"numero": "1", "color": (255, 0, 0), "desc": "Rojo - El perseguidor."},
                {"nombre": "Pinky", "numero": "2",  "color": (255, 182, 193), "desc": "Rosa - El emboscador."},
                {"nombre": "Inky", "numero": "3", "color": (0, 255, 255), "desc": "Celeste - El flanqueador."},
                {"nombre": "Clyde", "numero": "4", "color": (255, 165, 0), "desc": "Naranja - El tímido."},
                {"nombre": "Spike", "numero": "5","color": (0, 255, 0), "desc": "Verde - El interceptor."},
                {"nombre": "Coward", "numero": "6", "color": (128, 0, 128), "desc": "Violeta - El cobarde."}
            ]
        self.fantasmas_seleccionados = []
        self.esquinas_fantasma = []
        self.posicion_fantasma_seleccionado = 0
        
        # logica para temporizadores de fases globales de persecucion y dispersion
        self.fases_fantasmas = [
            ('scatter', 7),
            ('chase', 20),
            ('scatter', 7),
            ('chase', 20),
            ('scatter', 5),
            ('chase', 20),
            ('scatter', 5),
            ('chase', 1000000000)
        ]
        self.fase_actual = 0
        self.tiempo_fase_actual = 0.0
        self.fantasmas_comidos_ronda = 0
        self.fantasmas_activos = []
        self.puntos_comidos_nivel = 0
        
        self.empezar_mapa() # llamamos a la funcion para empezar el juego

    def pantalla_inicio(self):
        """
        Funcion para mostrar la pantalla de inicio
        """
        self.pantalla.fill((0,0,0))
        fuente_pacman = pygame.font.SysFont("Courier", 60)  # seteamos la fuente para el txto
        fuente_high_score = pygame.font.SysFont("Courier", 30)
        texto_Pacman = fuente_pacman.render("PAC-MAN", True, (255, 255, 0))  # guardamos el texto
        high_score = self.puntaje.cargar_high_score()  # guardamos el puntaje maximo usando la funcion de cargar ese valor
        texto_high_score = fuente_high_score.render(f"HIGH SCORE", True, (255, 255, 255))
        texto_high_score_numero = fuente_high_score.render(f"{high_score}", True, (255, 255, 0))
        texto_enter = fuente_high_score.render("Presione enter para jugar", True, (255, 255, 255))
        self.pantalla.blit(texto_Pacman, (160,200))
        self.pantalla.blit(texto_high_score, (175,30))  # 
        self.pantalla.blit(texto_high_score_numero, (240,80))
        if self.mostrar_enter == True: #si mostrar es ture mostramos el texto de enter todo  esto para que titile
            self.pantalla.blit(texto_enter, (65,425))
        self.fps_por_texto_enter += 1 #sumamos uno por cada fps
        if self.fps_por_texto_enter >= 120: 
            self.mostrar_enter = not self.mostrar_enter # invertimos valor cada 240 fps cada 4 segundos 60*4
            self.fps_por_texto_enter = 0    #volvemos a cero apra reiniciar los 4 segundos
        claves = pygame.key.get_pressed()
        if claves[pygame.K_RETURN]:  # si se presiona enter
            self.estado = "Elegir Fantasmas"   #cambiamos valor del estado a elegir fantasmas 
        pygame.display.flip()

    def elegir_fantasmas(self):  
        """
        Funcion para elegir los fantasmas
        """
        self.pantalla.fill((0,0,0))
        fuente_texto_fantasma = pygame.font.SysFont("Courier", 30)
        fuente_fantasmas = pygame.font.SysFont("Courier", 25)
        fuente_descripcion = pygame.font.SysFont("Courier", 20)  #seteamos fuentes
        poscion_y = 200 #poscion en la que empiezan los nombres de los fantasmas 
        for fantasma in self.fantasmas:
            numero = f"{fantasma['numero']}"
            nombre_fantasma = f"{fantasma['nombre']}"
            color_fantasma = fantasma["color"]
            descripcion_fantasma = f"{fantasma['desc']}"
            texto_nombre_fantasma = fuente_fantasmas.render(nombre_fantasma, True,color_fantasma)
            texto_descripcion_fantasma = fuente_descripcion.render(descripcion_fantasma, True, (255, 255, 255))
            texto_numero_fantasma = fuente_fantasmas.render(numero, True, (255, 255, 255))
            self.pantalla.blit(texto_nombre_fantasma,(100, poscion_y))
            self.pantalla.blit(texto_descripcion_fantasma,(100, poscion_y + 25))
            self.pantalla.blit(texto_numero_fantasma,(80, poscion_y))
            pygame.draw.circle(self.pantalla, color_fantasma, (60, poscion_y + 15), 10)            
            poscion_y += 50
        poscion_y_rectangulo = 200
        alto_rectangulo = 50
        for i in (self.fantasmas_seleccionados):
            if i == 1:
                rectangulo_blanco = pygame.Rect(70, poscion_y_rectangulo , 450, alto_rectangulo)
                pygame.draw.rect(self.pantalla,(255, 255, 255), rectangulo_blanco, 2)
            elif i == 2:
                rectangulo_blanco = pygame.Rect(70, poscion_y_rectangulo + 50, 450, alto_rectangulo)
                pygame.draw.rect(self.pantalla,(255, 255, 255), rectangulo_blanco, 2)
            elif i == 3:
                rectangulo_blanco = pygame.Rect(70, poscion_y_rectangulo + 100, 450, alto_rectangulo)
                pygame.draw.rect(self.pantalla,(255, 255, 255), rectangulo_blanco, 2)
            elif i == 4:
                rectangulo_blanco = pygame.Rect(70, poscion_y_rectangulo + 150, 450, alto_rectangulo)
                pygame.draw.rect(self.pantalla,(255, 255, 255), rectangulo_blanco, 2)
            elif i == 5:
                rectangulo_blanco = pygame.Rect(70, poscion_y_rectangulo + 200, 450, alto_rectangulo)
                pygame.draw.rect(self.pantalla,(255, 255, 255), rectangulo_blanco, 2)
            elif i == 6:
                rectangulo_blanco = pygame.Rect(70, poscion_y_rectangulo + 250, 450, alto_rectangulo)
                pygame.draw.rect(self.pantalla,(255, 255, 255), rectangulo_blanco, 2)

        canitidad_elegida_fantasmas = fuente_texto_fantasma.render(f"Elegi 4 fantasmas [{len(self.fantasmas_seleccionados)}/4]", True, (255, 255, 0))
        self.pantalla.blit(canitidad_elegida_fantasmas, (50, 30))
        clave_inicio = pygame.key.get_pressed()
        if len(self.fantasmas_seleccionados) == 4 and clave_inicio[pygame.K_RETURN]:         
            self.estado = "Esquinas Fantasmas"
   

        pygame.display.flip()

    def esquinas_fantasmas(self):
        """
        Funcion para mostrar las esquinas de los fantasmas
        """
        self.pantalla.fill((0,0,0))
        fuente_texto = pygame.font.SysFont("Courier", 25)
        fuente_esquinas = pygame.font.SysFont("Courier", 25)
        fantasma_actual_inidce = self.fantasmas_seleccionados[self.posicion_fantasma_seleccionado]
        nombre_fantasma_actual = f"{self.fantasmas[fantasma_actual_inidce - 1]['nombre']}"
        color_fantasma_actual = self.fantasmas[fantasma_actual_inidce - 1]["color"]   
        esquinas = ["Arriba Izquierda", "Arriba Derecha", "Abajo Izquierda", "Abajo Derecha"]
        poscion_y = 200
        num = 1
        texto_eleccion = fuente_texto.render(f"Asigná una esquina a {nombre_fantasma_actual} [{len(self.esquinas_fantasma)}/4]", True, color_fantasma_actual)
        self.pantalla.blit(texto_eleccion, (35, 50))
        esquinas_usadas = []
        for i in self.esquinas_fantasma:
            esquinas_usadas.append(i["esquina"])
        for esquina in esquinas:
            if esquina in esquinas_usadas:
                color_esquina = (128, 128, 128)
                self.pantalla.blit(fuente_esquinas.render(f"{num}.", True, color_esquina), (150, poscion_y))
                self.pantalla.blit(fuente_esquinas.render(esquina, True, color_esquina), (180, poscion_y))
            else:
                self.pantalla.blit(fuente_esquinas.render(f"{num}.", True, (255, 255, 255)), (150, poscion_y))
                self.pantalla.blit(fuente_esquinas.render(esquina, True, (255, 255, 255)), (180, poscion_y))
            poscion_y += 75
            num += 1
        

        pygame.display.flip()

    def empezar_mapa(self):
        """
        Funcion para crear el mapa del juego instanciando la nueva clase Mapa
        """
        self.mapa = Mapa("mapa.txt")
        self.comida_faltante = self.mapa.comida_faltante
        
        self.personajes = Personajes(self.mapa, self.pantalla)  # creamos un objeto de la clase Personajes para el mapa
        self.pacman = Pacman(self.mapa.poscion_x_pacman, self.mapa.poscion_y_pacman, self.mapa, self.pantalla) # creamos un objeto de la clase Pacman con la posicion de pacman en el mapa y el mapa y la pantalla

        if self.estado == "Juego":  # recreamos los fantasmas si el mapa se resetea por pasar de nivel
            self.crear_fantasmas()

    def crear_fantasmas(self):
        """
        Funcion para instanciar las subclases de Fantasma de acuerdo a los seleccionados
        """
        self.fantasmas_activos = []
        fila_casa = 14
        columna_casa = 13

        esquinas_en_mapa = {
            "Arriba Izquierda": (1, 1),
            "Arriba Derecha": (1, largo_fila - 2),
            "Abajo Izquierda": (alto_mapa - 2, 1),
            "Abajo Derecha": (alto_mapa - 2, largo_fila - 2)
        }

        blinky_guardado = None


        for i in range(len(self.fantasmas_seleccionados)):
            numero_de_fantasma = self.fantasmas_seleccionados[i]
            nombre_fantasma = self.fantasmas[numero_de_fantasma - 1]["nombre"]
            
            esquina_actual = (1, 1)
            for esquina in self.esquinas_fantasma:
                if esquina["nombre"] == nombre_fantasma:
                    esquina_actual = esquinas_en_mapa.get(esquina["esquina"], (1, 1))
                    break
            
            nuevo_fantasma = None
            if numero_de_fantasma == 1:
                nuevo_fantasma = Blinky(self.mapa, columna_casa, fila_casa, esquina_actual,self.pantalla)
                blinky_guardado = nuevo_fantasma
            elif numero_de_fantasma == 2:
                nuevo_fantasma = Pinky(self.mapa, columna_casa + 1, fila_casa, esquina_actual,self.pantalla)
            elif numero_de_fantasma == 3:
                nuevo_fantasma = Inky(self.mapa, columna_casa, fila_casa, esquina_actual, self.pantalla,blinky_guardado)
            elif numero_de_fantasma == 4:
                nuevo_fantasma = Clyde(self.mapa, columna_casa - 1, fila_casa, esquina_actual,self.pantalla)
            elif numero_de_fantasma == 5:
                nuevo_fantasma = Spike(self.mapa, columna_casa, fila_casa, esquina_actual,self.pantalla)
            elif numero_de_fantasma == 6:
                nuevo_fantasma = Coward(self.mapa, columna_casa, fila_casa, esquina_actual,self.pantalla)           
            if nuevo_fantasma is not None:
                self.fantasmas_activos.append(nuevo_fantasma)
        for i in range(len(self.fantasmas_activos)):
            self.fantasmas_activos[i].orden_salida = i


    def posiciones_iniciales(self):
        """
        Funcion para reiniciar a los personajes tras perder una vida
        """
        self.pacman.x = self.mapa.poscion_x_pacman * tamaño_pixel
        self.pacman.y = self.mapa.poscion_y_pacman * tamaño_pixel
        self.pacman.direccion = ""
        self.pacman.proxima_direccion = ""
        self.pacman.direccion_para_imagen = "derecha"
        for fantasma in self.fantasmas_activos:
            fantasma.x = fantasma.x_inicial
            fantasma.y = fantasma.y_inicial
            fantasma.direccion = "arriba"
            fantasma.salio = False
            fantasma.ojos = False
            fantasma.esta_asustado = False
            fantasma.tiempo_asustado = 0

    def actualizar_fases_modo(self, dt):
        """
        Funcion para alternar ciclicamente entre el modo Scatter y Chase
        """
        if self.fase_actual >= len(self.fases_fantasmas):
            return
        
        modo, duracion = self.fases_fantasmas[self.fase_actual]
        for fantasma in self.fantasmas_activos:
            fantasma.modo = modo

        algun_asustado = False
        for fantasma in self.fantasmas_activos:
            if fantasma.esta_asustado == True:
                algun_asustado = True
                break

        if algun_asustado == True:
            return

        self.tiempo_fase_actual += dt
        if self.tiempo_fase_actual >= duracion:
            self.tiempo_fase_actual = 0.0
            self.fase_actual += 1
            for fantasma in self.fantasmas_activos:
                if fantasma.direccion == "izquierda": 
                    fantasma.direccion = "derecha"
                elif fantasma.direccion == "derecha":
                    fantasma.direccion = "izquierda"
                elif fantasma.direccion == "arriba":
                    fantasma.direccion = "abajo"
                elif fantasma.direccion == "abajo":
                    fantasma.direccion = "arriba"

    def correr_juego(self):               
        """
        Funcion para correr el juego
            
        """
        running = True # seteamos la variable running de qu8e esta corriendo el juego a true
        while running: # mientras el juego este corriendo
            dt = self.fps.tick(60) / 1000.0  # en segundos
            for event in pygame.event.get():  # obtenemos los eventos para ver si cierra la pantalla la persona
                if event.type == pygame.QUIT:  # si la persona cierra la pantalla
                    running = False  # seteamos running a false para que pare el juego
                if event.type == pygame.KEYDOWN and self.estado == "Elegir Fantasmas": # si el estado es elegir fantasmas
                    if len(self.fantasmas_seleccionados) < 4: # si la cantidad de fantasmas seleccionados es menos de 4
                        if event.key == pygame.K_1: # si la persona presiona 1
                            if 1 not in self.fantasmas_seleccionados: # si el fantasma no esta en la lista de fantasmas seleccionados
                                self.fantasmas_seleccionados.append(1) # agregamos el fantasma a la lista de fantasmas seleccionados
                        elif event.key == pygame.K_2: # si la persona presiona 2
                            if 2 not in self.fantasmas_seleccionados: # si el fantasma no esta en la lista de fantasmas seleccionados
                                self.fantasmas_seleccionados.append(2) # agregamos el fantasma a la lista de fantasmas seleccionados
                        elif event.key == pygame.K_3: # si la persona presiona 3
                            if 3 not in self.fantasmas_seleccionados: # si el fantasma no esta en la lista de fantasmas seleccionados
                                self.fantasmas_seleccionados.append(3) # agregamos el fantasma a la lista de fantasmas seleccionados
                        elif event.key == pygame.K_4: # si la persona presiona 4
                            if 4 not in self.fantasmas_seleccionados: # si el fantasma no esta en la lista de fantasmas seleccionados
                                self.fantasmas_seleccionados.append(4) # agregamos el fantasma a la lista de fantasmas seleccionados
                        elif event.key == pygame.K_5: # si la persona presiona 5
                            if 5 not in self.fantasmas_seleccionados: # si el fantasma no esta en la lista de fantasmas seleccionados
                                self.fantasmas_seleccionados.append(5) # agregamos el fantasma a la lista de fantasmas seleccionados
                        elif event.key == pygame.K_6: # si la persona presiona 6
                            if 6 not in self.fantasmas_seleccionados: # si el fantasma no esta en la lista de fantasmas seleccionados
                                self.fantasmas_seleccionados.append(6) # agregamos el fantasma a la lista de fantasmas seleccionados
                if event.type == pygame.KEYDOWN and self.estado == "Esquinas Fantasmas": # si el estado es esquinas de fantasmas
                    fantasma_en_seleccionado_inidce = self.fantasmas_seleccionados[self.posicion_fantasma_seleccionado]
                    nombre_fantasma_seleccionado = self.fantasmas[fantasma_en_seleccionado_inidce - 1]["nombre"]
                    if event.key == pygame.K_1:
                        self.esquinas_fantasma.append({"nombre": nombre_fantasma_seleccionado, "esquina": "Arriba Izquierda"})
                        self.posicion_fantasma_seleccionado += 1
                    elif event.key == pygame.K_2:
                        self.esquinas_fantasma.append({"nombre": nombre_fantasma_seleccionado, "esquina": "Arriba Derecha"})
                        self.posicion_fantasma_seleccionado += 1
                    elif event.key == pygame.K_3:
                        self.esquinas_fantasma.append({"nombre": nombre_fantasma_seleccionado, "esquina": "Abajo Izquierda"})
                        self.posicion_fantasma_seleccionado += 1
                    elif event.key == pygame.K_4:
                        self.esquinas_fantasma.append({"nombre": nombre_fantasma_seleccionado, "esquina": "Abajo Derecha"})
                        self.posicion_fantasma_seleccionado += 1
                    if self.posicion_fantasma_seleccionado == len(self.fantasmas_seleccionados):
                        self.estado = "Juego"
                        self.crear_fantasmas()

            if self.estado == "Inicio": # si el estado es inicio
                self.pantalla_inicio()
                if not pygame.mixer.music.get_busy():  # solo reproducir si no está sonando
                    pygame.mixer.music.play(-1)
            elif self.estado == "Elegir Fantasmas": # si el estado es elegir fantasmas
                self.elegir_fantasmas()
            elif self.estado == "Esquinas Fantasmas": # si el estado es esquinas de fantasmas
                self.esquinas_fantasmas()
            elif self.estado == "Juego": # si el estado es juego
                self.pantalla.fill((0,0,0))  # seteamos la pantalla a negro
                pygame.mixer.music.load("musica_juego.mp3")
                if not pygame.mixer.music.get_busy():  # solo reproducir si no está sonando
                    pygame.mixer.music.play(-1) 
                
                
                self.mapa.dibujar(self.pantalla) 
                self.actualizar_fases_modo(dt)  

                if self.puntaje.vidas > 0:
                    self.pacman.dibujar(dt) # dibujamos pacman
                    score = self.pacman.comer(self.fantasmas_activos) # obtenemos el puntaje de la comida si el pacman come pasandole los fantasmas
                    if self.pacman.ver_power_pellet() == True: # verificamos si el power_pellet esta activo
                        velocidad =  2.25 # si esta activo seteamos la velocidad de pacman a 2.25
                    else:
                        velocidad = 2 # si no esta activo seteamos la velocidad de pacman a 2
                    self.pacman.mover(velocidad, dt) # movemos pacman 
                
                    if score == None: # si score es None
                        score = 0 # seteamos score a 0
                        self.puntaje.actualizar_puntaje(score) # actualizamos el puntaje
                    else:
                        self.puntaje.actualizar_puntaje(score) # actualizamos el puntaje
                        self.puntos_comidos_nivel += score
                        self.comida_faltante -= 1 # restamos 1 al contador de comida
                        if self.comida_faltante == 0: # si no quedan mas comida
                            self.puntaje.actualizar_lvl(1) # aumentamos el nivel
                            self.empezar_mapa() # llamamos a la funcion para empezar denuevo
                            self.puntos_comidos_nivel = 0

                    for fantasma in self.fantasmas_activos:
                        fila_pacman = int(self.pacman.y // tamaño_pixel)
                        columna_pacman = int(self.pacman.x // tamaño_pixel)
                        
                        fantasma.mover(fila_pacman, columna_pacman, self.pacman.direccion_para_imagen, dt, self.puntos_comidos_nivel)
                        fantasma.dibujar(self.pantalla)
                        
                        # calculamos colisiones por distancia euclidiana de pixeles
                        distancia_x = self.pacman.x - fantasma.x
                        distancia_y = self.pacman.y - fantasma.y
                        distancia = (distancia_x ** 2 + distancia_y ** 2) ** 0.5
                        
                        if distancia < 15: # colision cercana entre el pacman y un fantasma
                            if fantasma.esta_asustado == True:
                                self.fantasmas_comidos_ronda += 1
                                puntos_comer_fantasmas = 200 * (2 ** (self.fantasmas_comidos_ronda - 1))
                                if puntos_comer_fantasmas > 1600:
                                    puntos_comer_fantasmas = 1600
                                self.puntaje.actualizar_puntaje(puntos_comer_fantasmas)
                                
                                fantasma.esta_asustado = False
                                fantasma.ojos = True # mandamos los ojos del fantasma de regreso a casa
                            elif fantasma.ojos == False:
                                self.puntaje.vidas -= 1
                                self.sonido_muerte.play()
                                self.pacman.animacion_muerte()
                                pygame.time.delay(120)  
                                if self.puntaje.vidas > 0:
                                    self.posiciones_iniciales()
                                    self.puntos_comidos_nivel = 0
                                break
                    
                    if self.pacman.power_pellet == False:
                        self.fantasmas_comidos_ronda = 0 # se reinicia el contador si el modo asustado expiro

                self.puntaje.mostrar() # mostramos el puntaje y el puntaje maximo
                pygame.display.flip() # actualizamos la pantalla
        self.puntaje.actualizar_high_score() # guardamos el puntaje maximo cada que termina la partida
        pygame.quit() # cerramos la pantalla