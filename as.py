import pygame
paleta_colores = {
    "X" : (0,0,0),
    "." : (255,255,255),
    " " : (196, 181, 183),
    "G" : (21, 83, 201),
    "-" : (247, 22, 56),
    "o" : (255,255,255),
    "P" : (196, 181, 183),
    "T" : (18, 202, 247)
}
mapa = []
with open("a.txt" , "r") as f:
    for linea in f:
        mapa.append(list(linea.strip()))
        
largo_fila = 28
alto_mapa = 31
tamaño_pixel = 20
tamaño_score = 60
pantalla = pygame.display.set_mode((largo_fila * tamaño_pixel, (alto_mapa * tamaño_pixel) + tamaño_score))
def posicion_pacman(mapa):
    for fila in range(alto_mapa):
        for columna in range(largo_fila):
            if mapa[fila][columna] == "P":
                return columna, fila
class Personajes:   
    def __init__(self,mapa):
        self.mapa = mapa 

class Pacman(Personajes):
    def __init__(self,x,y):
        Personajes.__init__(self,mapa)
        self.x = x * tamaño_pixel
        self.y = y * tamaño_pixel   
        self.power_pellet = False
        self.tiempo_de_power_pellet = 0
        self.direccion = ""
        self.proxima_direccion = ""
        
    def mover(self,velocidad):
        claves = pygame.key.get_pressed()            
        velocidad_tiles = 1
        if claves[pygame.K_LEFT]:
            self.proxima_direccion = "izquierda"
        elif claves[pygame.K_RIGHT]:
            self.proxima_direccion = "derecha"
        elif claves[pygame.K_UP]:
            self.proxima_direccion = "arriba"
        elif claves[pygame.K_DOWN]:
            self.proxima_direccion = "abajo"
        if self.x % tamaño_pixel == 0 and self.y % tamaño_pixel == 0:
            proxima_doblar_x = self.x // tamaño_pixel
            proxima_doblar_y = self.y // tamaño_pixel

            if self.proxima_direccion == "izquierda":
                proxima_doblar_x -= velocidad_tiles
            elif self.proxima_direccion == "derecha":
                proxima_doblar_x += velocidad_tiles
            elif self.proxima_direccion == "arriba":
                proxima_doblar_y -= velocidad_tiles
            elif self.proxima_direccion == "abajo":
                proxima_doblar_y += velocidad_tiles


            if self.mapa[proxima_doblar_y ][proxima_doblar_x % largo_fila] != "X":
                self.direccion = self.proxima_direccion

            proximo_bloque_adelante_x = self.x // tamaño_pixel
            proximo_bloque_adelante_y = self.y // tamaño_pixel

            if self.direccion == "izquierda":
                proximo_bloque_adelante_x -= velocidad_tiles
            elif self.direccion == "derecha":
                proximo_bloque_adelante_x += velocidad_tiles
            elif self.direccion == "arriba":
                proximo_bloque_adelante_y -= velocidad_tiles
            elif self.direccion == "abajo":
                proximo_bloque_adelante_y += velocidad_tiles


            if self.mapa[proximo_bloque_adelante_y][proximo_bloque_adelante_x % largo_fila] == "X":
                self.direccion = ""

        if self.direccion == "izquierda":
            self.x -= velocidad
        elif self.direccion == "derecha":
            self.x += velocidad
        elif self.direccion == "arriba":
            self.y -= velocidad
        elif self.direccion == "abajo":
            self.y += velocidad
        if self.x < 0:
            self.x = (largo_fila-1) * tamaño_pixel
        elif self.x > (largo_fila-1) * tamaño_pixel:
            self.x = 0
        self.x = round(self.x)
        self.y = round(self.y)

        

       
    def comer(self):
        if self.x % tamaño_pixel == 0 and self.y % tamaño_pixel == 0:
            fila = self.y // tamaño_pixel
            columna = self.x // tamaño_pixel
            if self.mapa[fila][columna] == ".":
                self.mapa[fila][columna] = " "
                return 10
            elif self.mapa[fila][columna] == "o":
                self.mapa[fila][columna] = " "
                self.power_pellet = True
                self.tiempo_de_power_pellet = 270   
                return 50
    def ver_power_pellet(self):
        if self.tiempo_de_power_pellet > 0:
            self.tiempo_de_power_pellet -= 1
            if self.tiempo_de_power_pellet == 0:
                self.power_pellet = False
                return self.power_pellet
            else:
                self.power_pellet = True
                return self.power_pellet
        else:
            self.power_pellet = False
            return self.power_pellet
        
    def dibujar(self):
        pygame.draw.circle(pantalla,(255, 217, 0), (self.x +10, self.y + tamaño_score - 10 + 10 ), 10)
class fantasmas(Personajes):
    def __init__(self):
        Personajes.__init__(self,mapa)

class Puntaje:
    def __init__(self, score):
        self.puntos = score
    def actualizar(self, score):
        self.puntos += score
        return self.puntos
    def mostrar(self, max_score):
        fuente = pygame.font.SysFont("Courier", 40)
        texto_score = fuente.render(f"{self.puntos}", True, (255, 255, 255))
        texto_high_score_texto = fuente.render("HIGH SCORE", True, (255, 255, 255))
        texto_high_score = fuente.render(f"{max_score}", True, (255, 255, 255))
        pantalla.blit(texto_score, (30,30))
        pantalla.blit(texto_high_score_texto, (175,0))
        pantalla.blit(texto_high_score, (175,30))
        return max_score

    
px,py = posicion_pacman(mapa)
Personajes(mapa)
pacman = Pacman(px,py)

def crear_mapa(mapa,pantalla):
    pygame.init()
    fps =  pygame.time.Clock()
    puntaje = Puntaje(0)
    movimiento = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pantalla.fill((0,0,0))
        for fila in range(alto_mapa):
            for columna in range(largo_fila):
                color = paleta_colores[mapa[fila][columna]]
                lugar = (columna * tamaño_pixel, fila * tamaño_pixel + tamaño_score -10, tamaño_pixel, tamaño_pixel)
                centro_x = columna * tamaño_pixel + tamaño_pixel // 2
                centro_y = fila * tamaño_pixel + tamaño_pixel // 2 + tamaño_score -10
                centro_pixel = (centro_x, centro_y)      
                if mapa[fila][columna] == ".":
                    pygame.draw.rect(pantalla,(196, 181, 183),lugar)
                    pygame.draw.circle(pantalla,color,centro_pixel, 2)
                elif mapa[fila][columna] == "o":
                    pygame.draw.rect(pantalla,(196, 181, 183),lugar)
                    pygame.draw.circle(pantalla,color,centro_pixel, 4)
                else:
                    pygame.draw.rect(pantalla,color,lugar)
                    
        pacman.dibujar()
        movimiento += 1
        score = pacman.comer()
        if pacman.ver_power_pellet() == True:
            velocidad = 1.25
        else:
            velocidad = 1
        pacman.mover(velocidad)
     
        if score == None:
            score = 0
            puntos_actuales = puntaje.actualizar(score)
        else:
            puntos_actuales = puntaje.actualizar(score)
        max_score = 0
        if puntos_actuales > max_score:
            max_score = puntos_actuales
        puntaje.mostrar(max_score)
        pygame.display.flip()
        fps.tick(60) 
    pygame.quit()
crear_mapa(mapa, pantalla)

