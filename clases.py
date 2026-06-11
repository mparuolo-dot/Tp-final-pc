import pygame
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
alto_mapa = 31      #seteamos los parametros del mapa y agregados y el tamaño de los pixeles
tamaño_pixel = 20
tamaño_score = 60



class Personajes:   
    """
    clase para los personajes del juego
    
    Args:
        mapa (list): mapa del juego
    """
    def __init__(self,mapa,pantalla):
        self.mapa = mapa  
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

    

        

       
    def comer(self) -> int: 
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
    
        



class fantasmas(Personajes):
    def __init__(self):
        Personajes.__init__(self)

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

        if self.vidas == 0: # si no quedan vidas
            self.pantalla.fill((0,0,0))
            fuente = pygame.font.SysFont("Courier", 60)  # seteamos la fuente para el txto
            texto_game_over = fuente.render("GAME OVER", True, (255, 255, 255)) # guardamos el mensaje game over
            self.pantalla.blit(texto_game_over, (120,275)) # mostramos el mensaje game over
        elif self.vidas == 1: # si quedan 1 vidas
            pygame.draw.circle(self.pantalla,(255, 217, 0), (50, 675), 10) # dibujamos las vidas en la pantalla
        elif self.vidas == 2: # si quedan 2 vidas
            pygame.draw.circle(self.pantalla,(255, 217, 0), (50, 675), 10) # dibujamos las vidas en la pantalla
            pygame.draw.circle(self.pantalla,(255, 217, 0), (80, 675), 10)
        elif self.vidas == 3: # si quedan 3 vidas
            pygame.draw.circle(self.pantalla,(255, 217, 0), (50, 675), 10)
            pygame.draw.circle(self.pantalla,(255, 217, 0), (80, 675), 10)   # dibujamos las vidas en la pantalla
            pygame.draw.circle(self.pantalla,(255, 217, 0), (110, 675), 10)


class Juego:
    def __init__(self):
        """
        Funcion para iniciar el juego
        """
        pygame.init()  # inicializamos la pantalla del pygame
        self.pantalla = pygame.display.set_mode((largo_fila * tamaño_pixel, (alto_mapa * tamaño_pixel) + tamaño_score + 30))  # creamse la pantalla del juego
        self.fps =  pygame.time.Clock() # creamos un objeto que usamos para los fps
        self.puntaje = Puntaje(0, self.pantalla) # creamos un objeto de la clase Puntaje y lo seteamos para que empeize en 0 
        self.empezar_mapa() # llamamos a la funcion para empezar el juego
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
        texto_enter = fuente_high_score.render("Presione enter para jugar", True, (255, 255,255))
        self.pantalla.blit(texto_Pacman, (160,200))
        self.pantalla.blit(texto_high_score, (175,30))  # 
        self.pantalla.blit(texto_high_score_numero, (240,80))
        if self.mostrar_enter == True: #si mostrar es ture mostramos el texto de enter todo  esto para que titile
            self.pantalla.blit(texto_enter, (65,425))
        self.fps_por_texto_enter += 1 #sumamos uno por cada fps
        if self.fps_por_texto_enter >= 240: 
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
        Funcion para crear el mapa del juego
        """
        self.mapa = []
        self.comida_faltante = 0
        ghost_house = False
        pacman_existencia = False
        try:
            with open("mapa.txt" , "r") as f:  # abrimos el archivo de texto con el mapa
                for linea in f:
                    self.mapa.append(list(linea.strip())) # guardamos cada linea de texto(fila) en una lista 
                if len(self.mapa) != alto_mapa: # si el tamaño de la fila es diferente al tamaño del mapa establecido
                    raise ValueError("El alto del mapa es incorrecto")         
                for fila in range(alto_mapa):
                    if len(self.mapa[fila]) != largo_fila: # si el tamaño de la filaes diferente al tamaño del mapa establecido
                        raise ValueError("El largo del mapa es incorrecto")
                    for columna in range(largo_fila):
                        if self.mapa[fila][columna] not in paleta_colores.keys(): # si el caracter no esta en los posibles cracteres
                            raise ValueError(f"El caracter {self.mapa[fila][columna]} es desconocido")
                        if self.mapa[fila][columna] == "G": # si el caracter es Ghost house
                            ghost_house = True # seteamos la variable ghost_house a true
                        if self.mapa[fila][columna] == "P": # si el caracter es pacman
                            pacman_existencia = True # seteamos la variable pacman_existencia a true
                if ghost_house == False: # si no hay ghost house
                    raise ValueError("No hay ghost house")
                if pacman_existencia == False: # si no hay pacman
                    raise ValueError("No hay pacman")
                            
        except FileNotFoundError:
            raise FileNotFoundError("No se encontro el archivo")
        
        poscion_x_pacman = 0
        poscion_y_pacman = 0
        for fila in range(alto_mapa):
            for columna in range(largo_fila):      #buscamos la posicion de pacman en el mapa
                if self.mapa[fila][columna] == "P":
                    poscion_x_pacman = columna
                    poscion_y_pacman = fila             # obtenemos la posicion de pacman en el mapa
                elif self.mapa[fila][columna] == "." or self.mapa[fila][columna] == "o":
                    self.comida_faltante += 1  # contamos la cantidad de comida en el mapa
        self.personajes = Personajes(self.mapa, self.pantalla)  # creamos un objeto de la clase Personajes para el mapa
        self.pacman = Pacman(poscion_x_pacman,poscion_y_pacman,self.mapa, self.pantalla) # creamos un objeto de la clase Pacman con la posicion de pacman en el mapa y el mapa y la pantalla


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

            if self.estado == "Inicio": # si el estado es inicio
                self.pantalla_inicio()
            elif self.estado == "Elegir Fantasmas": # si el estado es elegir fantasmas
                self.elegir_fantasmas()
            elif self.estado == "Esquinas Fantasmas": # si el estado es esquinas de fantasmas
                self.esquinas_fantasmas()
            elif self.estado == "Juego": # si el estado es juego
                self.pantalla.fill((0,0,0))  # seteamos la pantalla a negro
                for fila in range(alto_mapa):  
                    for columna in range(largo_fila):   # recorremos el mapa
                        color = paleta_colores[self.mapa[fila][columna]]  # obtenemos el color de la paleta de colores de cada fila,columna
                        lugar = (columna * tamaño_pixel, fila * tamaño_pixel + tamaño_score -10, tamaño_pixel, tamaño_pixel)  # creamos el rectangulo.rect de cada tile
                        centro_x = columna * tamaño_pixel + tamaño_pixel // 2 
                        centro_y = fila * tamaño_pixel + tamaño_pixel // 2 + tamaño_score -10  # obtenemos el centro de cada tile en y tenemos en cuento el tamaño del score
                        centro_pixel = (centro_x, centro_y)    #guardamops el centro de cada tile   
                        if self.mapa[fila][columna] == ".": # si el tile es comida chica
                            pygame.draw.rect(self.pantalla,(196, 181, 183),lugar) # dibujamos el tile en gris
                            pygame.draw.circle(self.pantalla,color,centro_pixel, 2)  # dibujamos la comida arriba de ese tile en el centro
                        elif self.mapa[fila][columna] == "o": # si el tile es comida grande
                            pygame.draw.rect(self.pantalla,(196, 181, 183),lugar) # dibujamos el tile en gris
                            pygame.draw.circle(self.pantalla,color,centro_pixel, 4)  # dibujamos la comida arriba de ese tile en el centro
                        else:
                            pygame.draw.rect(self.pantalla,color,lugar) # para cualquier otro elemento en base a su palaeta de colores y posciion lo dibujamos en panatlla
                self.pacman.dibujar(dt) # dibujamos pacman
                score = self.pacman.comer() # obtenemos el puntaje de la comida si el pacman come
                if self.pacman.ver_power_pellet() == True: # verificamos si el power_pellet esta activo
                    velocidad =  2.25 # si esta activo seteamos la velocidad de pacman a 2
                else:
                    velocidad = 2 # si no esta activo seteamos la velocidad de pacman a 1
                self.pacman.mover(velocidad, dt) # movemos pacman 
            
                if score == None: # si score es None
                    score = 0 # seteamos score a 0
                    self.puntaje.actualizar_puntaje(score) # actualizamos el puntaje
                else:
                    self.puntaje.actualizar_puntaje(score) # actualizamos el puntaje
                    self.comida_faltante -= 1 # restamos 1 al contador de comida
                    if self.comida_faltante == 0: # si no quedan mas comida
                        self.puntaje.actualizar_lvl(1) # aumentamos el nivel
                        self.empezar_mapa() # llamamos a la funcion para empezar denuevo

                self.puntaje.mostrar() # mostramos el puntaje y el puntaje maximo
                pygame.display.flip() # actualizamos la pantalla
        self.puntaje.actualizar_high_score() # guardamos el puntaje maximo cada que termina la partida
        pygame.quit() # cerramos la pantalla

                
