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
        self.x = x 
        self.y = y      
        self.velocidad = 1
        self.direccion = ""
        self.proxima_direccion = ""
    def mover(self):
        claves = pygame.key.get_pressed()
        if claves[pygame.K_LEFT]:
            self.proxima_direccion = "izquierda"
        elif claves[pygame.K_RIGHT]:
            self.proxima_direccion = "derecha"
        elif claves[pygame.K_UP]:
            self.proxima_direccion = "arriba"
        elif claves[pygame.K_DOWN]:
            self.proxima_direccion = "abajo"
        
        proxima_x_posible = self.x
        proxima_y_posible = self.y
        if self.proxima_direccion == "izquierda":
            proxima_x_posible -= self.velocidad
        elif self.proxima_direccion == "derecha":
            proxima_x_posible += self.velocidad
        elif self.proxima_direccion == "arriba":
            proxima_y_posible -= self.velocidad
        elif self.proxima_direccion == "abajo":
            proxima_y_posible += self.velocidad

        if self.mapa[proxima_y_posible][proxima_x_posible] != "X" and self.mapa[proxima_y_posible][proxima_x_posible] != "T":
            self.direccion = self.proxima_direccion
        nueva_x = self.x
        nueva_y = self.y
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
        pixel_y = self.y * tamaño_pixel + tamaño_pixel // 2 + tamaño_score - 10
        pygame.draw.circle(pantalla,(255, 217, 0), (pixel_x, pixel_y), 10)
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
        if movimiento % 8 == 0:
            pacman.mover()
     
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

