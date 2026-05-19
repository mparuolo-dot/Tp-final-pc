import pygame
paleta_colores = {
    "X" : (0,0,0),
    "." : (255,255,255),
    " " : (196, 181, 183),
    "G" : (21, 83, 201),        # seteamos la paleta de colores para cada signo
    "-" : (247, 22, 56),
    "o" : (255,255,255),
    "P" : (196, 181, 183),
    "T" : (18, 202, 247)
}
mapa = []
with open("mapa.txt" , "r") as f:  # abrimos el archivo de texto con el mapa
    for linea in f:
        mapa.append(list(linea.strip())) # guardamos cada linea de texto(fila) en una lista 
        
largo_fila = 28
alto_mapa = 31      #seteamos los parametros del mapa y agregados y el tamaño de los pixeles
tamaño_pixel = 20
tamaño_score = 60

pantalla = pygame.display.set_mode((largo_fila * tamaño_pixel, (alto_mapa * tamaño_pixel) + tamaño_score))  # creamse la pantalla del juego

def posicion_pacman(mapa: list) -> tuple:
    """
    Funcion que busca la posicion de pacman en el mapa
    
    Args:
        mapa (list): mapa del juego
    
    Returns:
        tuple: posicion de pacman en el mapa
    """
    for fila in range(alto_mapa):
        for columna in range(largo_fila):      #buscamos la posicion de pacman en el mapa
            if mapa[fila][columna] == "P":
                return columna, fila
class Personajes:   
    """
    clase para los personajes del juego
    
    Args:
        mapa (list): mapa del juego
    """
    def __init__(self,mapa):
        self.mapa = mapa  

class Pacman(Personajes): 
    """
    clase para el pacman 
    
    Args:
        Personajes (class): clase para los personajes del juego
    """
    def __init__(self,x: int,y: int):
        """   
        Args:
            x (int): posicion x del pacman en tiles
            y (int): posicion y del pacman en tiles
        """
        Personajes.__init__(self,mapa)
        self.x = x * tamaño_pixel   # seteamos la posicion de pacman en pixeles cuando x e y los teniamos en tiles del mapa
        self.y = y * tamaño_pixel    
        self.power_pellet = False  #seteamos el valor de power_pellet 
        self.tiempo_de_power_pellet = 0 # seteamos el tiempo de duracion del power_pellet
        self.direccion = ""  # seteamos la direccion de pacman para usar en mover
        self.proxima_direccion = ""  # seteamos la proxima direccion de pacman para usar en mover
        
    def mover(self,velocidad : int):
        """
        Funcion para mover el pacman en la pantalla
        
        Args:
            velocidad (int): velocidad del pacman
        """
        claves = pygame.key.get_pressed()    # obtenemos las teclas presionadas         
        velocidad_tiles = 1 # seteamos la velocidad de pacman en tiles diferenciada de la velocidad en pixeles
        if claves[pygame.K_LEFT]:
            self.proxima_direccion = "izquierda" 
        elif claves[pygame.K_RIGHT]:
            self.proxima_direccion = "derecha" 
        elif claves[pygame.K_UP]:                       # Guardamos la proxima direccion de pacman en base al input de las teclas
            self.proxima_direccion = "arriba"
        elif claves[pygame.K_DOWN]:
            self.proxima_direccion = "abajo"
        if self.x % tamaño_pixel == 0 and self.y % tamaño_pixel == 0:    # verificamos si el pacman esta en el centro el tile en pixeles para qeu pueda dbolar asi no se superpone con paredes 
            proxima_doblar_x = self.x // tamaño_pixel
            proxima_doblar_y = self.y // tamaño_pixel   # para verificar las paredes y a donde tenemos que ir volvemos a pasar de pixeles a tiles

            if self.proxima_direccion == "izquierda":
                proxima_doblar_x -= velocidad_tiles
            elif self.proxima_direccion == "derecha":
                proxima_doblar_x += velocidad_tiles
            elif self.proxima_direccion == "arriba":   # dependiendo la direccion restamos o sumamos la velocidad de tiles a la proxima direccion
                proxima_doblar_y -= velocidad_tiles
            elif self.proxima_direccion == "abajo":
                proxima_doblar_y += velocidad_tiles


            if self.mapa[proxima_doblar_y ][proxima_doblar_x % largo_fila] != "X":  # verificamos si la proxima posicion a doblar es una pared y si no es guardamos la direccion
                self.direccion = self.proxima_direccion

            #la parte anteriror la usamos para verificar si podiamos doblar o no y la parte siguiente si no podemos doblar la usamos para ver si podemos avanzar en la direccion guardada

            proximo_bloque_adelante_x = self.x // tamaño_pixel
            proximo_bloque_adelante_y = self.y // tamaño_pixel  # para verificar las paredes y a donde tenemos que ir volvemos a pasar de pixeles a tiles

            if self.direccion == "izquierda":
                proximo_bloque_adelante_x -= velocidad_tiles
            elif self.direccion == "derecha":
                proximo_bloque_adelante_x += velocidad_tiles
            elif self.direccion == "arriba":                        # dependiendo la direccion restamos o summamos la velocidad de tiles a la proxima direccion
                proximo_bloque_adelante_y -= velocidad_tiles
            elif self.direccion == "abajo":
                proximo_bloque_adelante_y += velocidad_tiles


            if self.mapa[proximo_bloque_adelante_y][proximo_bloque_adelante_x % largo_fila] == "X": # vemos si el bloque al que avanzamos es una pared si es guarsdamops una direciion vacia para no movernos  usamos % largo_fila para que no se salga del mapa
                self.direccion = ""

        if self.direccion == "izquierda":
            self.x -= velocidad
        elif self.direccion == "derecha":
            self.x += velocidad
        elif self.direccion == "arriba":            # dependiendo la direccion restamos o summamos la velocidad en pixeles que es lo que mopstramos en pantalla
            self.y -= velocidad   
        elif self.direccion == "abajo":
            self.y += velocidad

        if self.x < 0:                            # si llegamos al tunel por la izquierda
            self.x = (largo_fila - 1) * tamaño_pixel  #seteamos posicion al tunel de la derecha
        elif self.x > (largo_fila - 1) * tamaño_pixel:   # si llegamos al tunel por derecha
            self.x = 0  #seteamos posicion al tunel de la izquierda

        self.x = round(self.x) #redondeamos la posicion de pacman para que cuando cambiemos de velocidades no afecre el movimiento de tiles
        self.y = round(self.y)

        

       
    def comer(self) -> int: 
        """
        Funcion para comer comida y devolver el valor de la comida
        
        Returns:
            int: valor de la comida
        """
        if self.x % tamaño_pixel == 0 and self.y % tamaño_pixel == 0:    # verificamos si el pacman esta en el centro el tile en pixeles para qeu pueda comer
            fila = self.y // tamaño_pixel
            columna = self.x // tamaño_pixel  # para verificar las comida pasamos de pixeles a tiles
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
        
    def dibujar(self):
        """
        Funcion para dibujar el pacman en la pantalla
        """
        pygame.draw.circle(pantalla,(255, 217, 0), (self.x +10, self.y + tamaño_score - 10 + 10 ), 10) # dibujamos el pacman en la pantalla teniendo en cuenta el espacio del score y el + 10 para que quede en el medio del tile

class fantasmas(Personajes):
    def __init__(self):
        Personajes.__init__(self,mapa)

class Puntaje:
    def __init__(self, score: int):
        """
        Args:
            score (int): puntaje del juego
        """
        self.puntos = score #seteamos el puntaje
        self.high_score =  self.cargar_high_score() # cargamos el puntaje maximo
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

    def mostrar(self):
        """
        Funcion para mostrar el puntaje en la pantalla
        
        """
        fuente = pygame.font.SysFont("Courier", 40)  # seteamos la fuente para el txto
        texto_score = fuente.render(f"{self.puntos}", True, (255, 255, 255)) # guardmaos los puntos
        texto_high_score_texto = fuente.render("HIGH SCORE", True, (255, 255, 255)) # guardamos el mensaje high score
        texto_high_score = fuente.render(f"{self.high_score}", True, (255, 255, 255)) # guradmaos el puntaje maximo
        pantalla.blit(texto_score, (30,30)) # mostramos los ountois en la pantalla
        pantalla.blit(texto_high_score_texto, (175,0)) # mostramos el mensaje highscore
        pantalla.blit(texto_high_score, (175,30)) # mostramos el puntaje maximo
 
    
px,py = posicion_pacman(mapa) # obtenemos la posicion de pacman en el mapa
Personajes(mapa) # creamos un objeto de la clase Personajes con el mapa
pacman = Pacman(px,py) # creamos un objeto de la clase Pacman con la posicion de pacman en el mapa

def crear_mapa(mapa: list,pantalla: pygame.surface.Surface):
    """
    Funcion para crear el mapa del juego e iterar sobre el
    
    Args:
        mapa (list): mapa del juego
        pantalla (pygame.surface.Surface): pantalla del juego
    """
    pygame.init()  # inicializamos la pantalla del pygame
    fps =  pygame.time.Clock() # creamos un objeto que usamos para los fps
    puntaje = Puntaje(0) # creamos un objeto de la clase Puntaje y lo seteamos para que empeize en 0
    running = True # seteamos la variable running de qu8e esta corriendo el juego a true
    contador_comida = 0 # seteamos el contador de comida en 0
    
    while running: # mientras el juego este corriendo
        for event in pygame.event.get():  # obtenemos los eventos para ver si cierra la pantalla la persona
            if event.type == pygame.QUIT:  # si la persona cierra la pantalla
                running = False  # seteamos running a false para que pare el juego
        pantalla.fill((0,0,0))  # seteamos la pantalla a negro
        for fila in range(alto_mapa):  
            for columna in range(largo_fila):   # recorremos el mapa
                color = paleta_colores[mapa[fila][columna]]  # obtenemos el color de la paleta de colores de cada fila,columna
                lugar = (columna * tamaño_pixel, fila * tamaño_pixel + tamaño_score -10, tamaño_pixel, tamaño_pixel)  # creamos el rectangulo.rect de cada tile
                centro_x = columna * tamaño_pixel + tamaño_pixel // 2 
                centro_y = fila * tamaño_pixel + tamaño_pixel // 2 + tamaño_score -10  # obtenemos el centro de cada tile en y tenemos en cuento el tamaño del score
                centro_pixel = (centro_x, centro_y)    #guardamops el centro de cada tile   
                if mapa[fila][columna] == ".": # si el tile es comida chica
                    pygame.draw.rect(pantalla,(196, 181, 183),lugar) # dibujamos el tile en gris
                    pygame.draw.circle(pantalla,color,centro_pixel, 2)  # dibujamos la comida arriba de ese tile en el centro
                    contador_comida += 1 # sumamos 1 al contador de comida chica
                elif mapa[fila][columna] == "o": # si el tile es comida grande
                    pygame.draw.rect(pantalla,(196, 181, 183),lugar) # dibujamos el tile en gris
                    pygame.draw.circle(pantalla,color,centro_pixel, 4)  # dibujamos la comida arriba de ese tile en el centro
                    contador_comida += 1 # sumamos 1 al contador de comida grande
                else:
                    pygame.draw.rect(pantalla,color,lugar) # para cualquier otro elemento en base a su palaeta de colores y posciion lo dibujamos en panatlla
                    
        pacman.dibujar() # dibujamos pacman
        score = pacman.comer() # obtenemos el puntaje de la comida si el pacman come
        if pacman.ver_power_pellet() == True: # verificamos si el power_pellet esta activo
            velocidad = 2 # si esta activo seteamos la velocidad de pacman a 2
        else:
            velocidad = 1 # si no esta activo seteamos la velocidad de pacman a 1
        pacman.mover(velocidad) # movemos pacman 
     
        if score == None: # si score es None
            score = 0 # seteamos score a 0
            puntaje.actualizar_puntaje(score) # actualizamos el puntaje
        else:
            puntaje.actualizar_puntaje(score) # actualizamos el puntaje
            contador_comida -= 1 # restamos 1 al contador de comida

        puntaje.mostrar() # mostramos el puntaje y el puntaje maximo
        pygame.display.flip() # actualizamos la pantalla
        fps.tick(60)  # seteamos los fps a 60
    puntaje.actualizar_high_score() # guardamos el puntaje maximo cada que termina la partida
    pygame.quit() # cerramos la pantalla

crear_mapa(mapa, pantalla) # creamos el mapa

