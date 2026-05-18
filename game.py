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

pantalla = pygame.display.set_mode((largo_fila * tamaño_pixel, alto_mapa * tamaño_pixel))
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
        self.x = x 
        self.y = y      
        self.tick_Rate = 150
        self.velocidad = 1
        self.direccion = ""
    def mover(self):
        pygame.time.delay(self.tick_Rate)
        claves = pygame.key.get_pressed()
        nueva_x = self.x
        nueva_y = self.y
        if claves[pygame.K_LEFT]:
            nueva_x -= self.velocidad
            self.direccion = "izquierda"
            if nueva_x <= 0:
                nueva_x = 0
        elif claves[pygame.K_RIGHT]:
            nueva_x += self.velocidad
            self.direccion = "derecha"
            if nueva_x >= 27:
                nueva_x = 27
        elif claves[pygame.K_UP]:
            nueva_y -= self.velocidad
            self.direccion = "arriba"
        elif claves[pygame.K_DOWN]:
            nueva_y += self.velocidad
            self.direccion = "abajo"
        else:
            if self.direccion == "izquierda":
                nueva_x -= self.velocidad
                if nueva_x <= 0:
                    nueva_x = 0
            elif self.direccion == "derecha":
                nueva_x += self.velocidad
                if nueva_x >= 27:
                    nueva_x = 27
            elif self.direccion == "arriba":
                nueva_y -= self.velocidad
            elif self.direccion == "abajo":
                nueva_y += self.velocidad
        if self.mapa[nueva_y][nueva_x] != "X" and self.mapa[nueva_y][nueva_x] != "T":
            self.x = nueva_x
            self.y = nueva_y
        elif self.mapa[nueva_y][nueva_x] == "T":
            if nueva_x <= 0:
                self.x = nueva_x + 27
                self.y = nueva_y 
            elif nueva_x >= 27:
                self.x = nueva_x - 27
                self.y = nueva_y
    def comer(self):
        if self.mapa[self.y][self.x] == ".":
            self.mapa[self.y][self.x] = " "
            return 10
        elif self.mapa[self.y][self.x] == "o":
            self.mapa[self.y][self.x] = " "
            return 50
        
    def dibujar(self):
        pixel_x = self.x * tamaño_pixel + tamaño_pixel // 2
        pixel_y = self.y * tamaño_pixel + tamaño_pixel // 2
        pygame.draw.circle(pantalla,(255, 217, 0), (pixel_x, pixel_y), 10)

class Puntaje:
    def __init__(self, score):
        self.puntos = score
    def actualizar(self, score):
        self.puntos += score
    def mostrar(self):
        fuente = pygame.font.SysFont("Arial", tamaño_pixel)
        texto = fuente.render(f"Score: {self.puntos}", True, (255, 255, 255))
        pantalla.blit(texto, (5,5))

px,py = posicion_pacman(mapa)
Personajes(mapa)
pacman = Pacman(px,py) 
def crear_mapa(mapa,pantalla):
    pygame.init()
    fps =  pygame.time.Clock()
    puntaje = Puntaje(0)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pantalla.fill((0,0,0))
        for fila in range(alto_mapa):
            for columna in range(largo_fila):
                color = paleta_colores[mapa[fila][columna]]
                lugar = (columna * tamaño_pixel, fila * tamaño_pixel, tamaño_pixel, tamaño_pixel)
                centro_x = columna * tamaño_pixel + tamaño_pixel // 2
                centro_y = fila * tamaño_pixel + tamaño_pixel // 2
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
        pacman.mover()
        score = pacman.comer()
        if score == None:
            score = 0
            puntaje.actualizar(score)
        else:
            puntaje.actualizar(score)
        puntaje.mostrar()
        pygame.display.flip()
        fps.tick(120) 
    pygame.quit()
crear_mapa(mapa, pantalla)

