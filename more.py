import pygame
import random

class mapa:
    def __init__(self, archivo):
        self.archivo = archivo
        self.mapa = self.generar_mapa()

    def generar_mapa(self):
        with open(self.archivo, 'r') as archivo:
            lineas = archivo.readlines()

        matriz = []
        for linea in lineas:
            linea = linea.strip('\n')
            fila = []
            for caracter in linea:
                fila.append(caracter)
            matriz.append(fila)
        return matriz
    def renderizar(self, screen):
        ts = 24
        for fil in range(len(self.mapa)):
            for col in range(len(self.mapa[fil])):
                x = col*ts
                y = fil*ts
                tile = self.mapa[fil][col]

                if tile == 'X':
                    pygame.draw.rect(screen, (0,0,0), (x, y, ts, ts))

                elif tile == '.' or tile=='o' or tile == 'P' or tile == ' ' or tile=='G' or tile =='-':
                    pygame.draw.rect(screen, (196, 181, 183), (x, y, ts, ts))

                    if tile =='.':
                        cx = x+ ts//2
                        cy = y + ts/2
                        pygame.draw.circle(screen, (255,255,255), (cx, cy), 3)
                    elif tile == 'o':
                        cx = x+ ts//2
                        cy = y + ts/2
                        pygame.draw.circle(screen, (255,255,255), (cx, cy), 7)
                    elif tile =='-':
                        pygame.draw.rect(screen, (255, 182, 193), (x, y + ts // 3, ts, ts // 3))
                elif tile == 'T':
                    pygame.draw.rect(screen, (18, 202, 247), (x, y, ts, ts))
    def posicion_pacman(self):
        for fil in range(len(self.mapa)):
            for col in range(len(self.mapa[fil])):
                if self.mapa[fil][col]== 'P':
                    return fil, col

    def es_libre(self, fil, col):
        if self.mapa[fil][col] != 'X' and self.mapa[fil][col] != 'G' and self.mapa[fil][col] != '-':
            return True
        return False
    def es_libre_casa(self, fil, col):
        return self.mapa[fil][col] != 'X' and self.mapa[fil][col] != 'G'
    def es_pellet(self, fil, col):
        return self.mapa[fil][col] == '.'
    def es_power(self, fil, col):
        return self.mapa[fil][col] == 'o'
    def es_tunnel(self,fil,col):
        return self.mapa[fil][col] == 'T'
    def es_ghost_house(self, fil, col):
        return self.mapa[fil][col] == 'G' or self.mapa[fil][col] == '-'
    def imprimir_score(self, score, screen):
        fuente = pygame.font.SysFont('arial', 24)
        texto = fuente.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(texto, (10, 10))

class pacman:
    def __init__(self, fil, col, mapa):
        self.fil = fil
        self.col = col
        self.x = col*24
        self.y = fil*24
        self.mapa = mapa
        self.actual_direc = (0,0)
        self.prox_direc = (0,0)
        self.score = 0
        self.timer = 0
        self.velocidad = 0.15
        self.vidas = 3
        self.power = False
    def dibujar(self, screen):
        cx = self.x + 24//2
        cy = self.y + 24//2
        pygame.draw.circle(screen, (255, 255, 0), (cx, cy), 10)
    def mover(self, fil, col, dt):
        self.timer+=dt
        if self.timer < self.velocidad:
            return
        self.timer = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  self.prox_direc = (0, -1)
        if keys[pygame.K_RIGHT]: self.prox_direc = (0,  1)
        if keys[pygame.K_UP]:    self.prox_direc = (-1, 0)
        if keys[pygame.K_DOWN]:  self.prox_direc = ( 1, 0)

        nf = self.fil + self.prox_direc[0]
        nc = self.col + self.prox_direc[1]
        
            
        if self.mapa.es_libre(nf, nc):
            self.fil = nf
            self.col = nc
            self.actual_direc = self.prox_direc
        else:
            nf = self.fil + self.actual_direc[0]
            nc = self.col + self.actual_direc[1]
            if self.mapa.es_libre(nf, nc):  
                self.fil = nf
                self.col = nc
        if self.mapa.es_tunnel(self.fil, self.col):
            if self.actual_direc == (0,1):
                self.col = 1
            else:
                self.col = len(self.mapa.mapa[self.fil]) - 2
        self.x = self.col * 24
        self.y = self.fil * 24
    def comer(self, fantasmas):
        if self.mapa.es_pellet( self.fil, self.col):
            self.mapa.mapa[self.fil][self.col]= ' '
            self.score += 10
        elif self.mapa.es_power( self.fil, self.col):
            self.mapa.mapa[self.fil][self.col]= ' '
            self.score += 50
            self.power = True
            for f in fantasmas:
                f.asustado()
            self.power = False
    def colision(self, fantasma):
        return self.fil == fantasma.fil and self.col == fantasma.col

class fantasma:
    def __init__(self, mapa):
        
        self.fil_inicial = 11
        self.col_inicial = 13
        self.fil = self.fil_inicial
        self.col = self.col_inicial
        self.x = self.col*24
        self.y = self.fil*24
        self.direccion = (0,1)
        self.mapa = mapa
        self.timer = 0
        self.velocidad = 0.2
        self.salio = False
        self.color = (0,0,0)
        self.esta_asustado = False
        self.tiempo_asustado = 0
        self.duracion_asustado = 6
        self.esquina = (0,0)
        self.modo = 'scatter'
        self.ojos = False
    def dibujar(self, screen):
        cx = self.x + 24//2
        cy = self.y + 24//2
        color = 0
        if self.ojos:
            pygame.draw.circle(screen, (255,255,255), (cx-3, cy),4)
            pygame.draw.circle(screen, (255,255,255), (cx+3, cy),4)
            return
        elif self.esta_asustado: color = (33, 33, 222)
        else: color = self.color
        pygame.draw.circle(screen, color , (cx, cy), 10)
    def target(self, p_fil, p_col, prox_direc):
        pass
    def aplicar_movimiento(self, direc):
        self.fil = self.fil + direc[0]
        self.col = self.col + direc[1]
        self.x = self.col * 24
        self.y = self.fil * 24
        self.direccion = direc
    def mover(self,p_fil, p_col, prox_direc, dt):
        self.timer+=dt
        if self.timer < self.velocidad:
            return
        self.timer = 0
        if self.mapa.es_ghost_house(self.fil, self.col):
            self.salio = False
            self.ojos = False
        if self.salio ==False:
            if not self.mapa.es_ghost_house(self.fil, self.col):
                self.salio = True
            else:
                self.fil -= 1
                self.x = self.col * 24
                self.y = self.fil * 24
            return


        direc_posibles = []
        parametro = self.mapa.es_libre_casa if self.ojos else self.mapa.es_libre
        if parametro(self.fil+1, self.col): direc_posibles.append((1, 0))
        if parametro(self.fil-1, self.col): direc_posibles.append((-1, 0))
        if parametro(self.fil, self.col+1): direc_posibles.append((0,1))
        if parametro(self.fil, self.col-1): direc_posibles.append((0, -1))
        direc_contraria = (-self.direccion[0], -self.direccion[1])
        if direc_contraria in direc_posibles: direc_posibles.remove(direc_contraria)

        if self.esta_asustado:
            self.tiempo_asustado += self.velocidad
            if self.tiempo_asustado>self.duracion_asustado:
                self.esta_asustado = False
                self.tiempo_asustado = 0
            else:
                direc = random.choice(direc_posibles)
                self.aplicar_movimiento(direc)
                return
   
        t_f , t_c = self.target(p_fil, p_col, prox_direc)
        if self.modo == 'scatter':
            t_f, t_c = self.esquina[0], self.esquina[1]
        if self.ojos:
            t_f , t_c= self.fil_inicial, self.col_inicial
        direccion = self.direccion
        menor_dist = 1000
        for direc in direc_posibles:
            nf = self.fil + direc[0]
            nc = self.col + direc[1]
            dist = ((t_f - nf)**2 + (t_c - nc)**2)**0.5
            if dist < menor_dist: 
                menor_dist = dist
                direccion = direc
        self.aplicar_movimiento(direccion)
        if self.mapa.es_tunnel(self.fil, self.col):
            self.velocidad = 0.5
            if self.direccion == (0,1):
                self.col = 1
            else:
                self.col = len(self.mapa.mapa[self.fil]) - 2
        else:
            self.velocidad = 0.2

    def asustado(self):
        self.esta_asustado = True
        self.duracion_asustado = 6
        self.tiempo_asustado = 0
        self.direccion = (-self.direccion[0], - self.direccion[1])

class blinky(fantasma):
    def __init__(self, mapa):
        super().__init__(mapa)
        self.color = (255,0,0)
        self.fil_inicial = 11
        self.col_inicial = 13
        self.fil = self.fil_inicial
        self.col = self.col_inicial
        self.esquina = (0, 27)
    def target(self, p_fil, p_col, prox_direc):
        return p_fil, p_col

class pinky(fantasma):
    def __init__(self, mapa):
        super().__init__(mapa)
        self.color = (255, 105, 180)
        self.fil_inicial = 12
        self.col_inicial = 13
        self.fil = self.fil_inicial
        self.col = self.col_inicial
        self.esquina = (0, 0)
    def target(self, p_fil, p_col, prox_direc):
        return p_fil + prox_direc[0]*4, p_col + prox_direc[1]*4

class clyde(fantasma):
    def __init__(self, mapa):
        super().__init__(mapa)
        self.color = (255, 182, 255)
        self.fil_inicial = 11
        self.col_inicial = 14
        self.fil = self.fil_inicial
        self.col = self.col_inicial
        self.esquina = (30, 27)
    def target(self, p_fil, p_col, prox_direc):
        dist = ((p_fil - self.fil)**2 + (p_col - self.col)**2)**0.5
        if dist>8:
            return p_fil, p_col
        else:
            #tengo que implementar el codigo para que el jugadro eliga el tile en scatter
            return len(self.mapa.mapa)-1, 0

class inky(fantasma):
    def __init__(self, mapa):
        super().__init__(mapa)
        self.color = (0, 255, 255)
        self.fil_inicial = 12
        self.col_inicial = 14
        self.fil = self.fil_inicial
        self.col = self.col_inicial
        self.esquina = (30, 0)
    def target(self, p_fil, p_col, prox_direc):
        #tengo que impelemantar si no esta blinky

        fil_t = p_fil + prox_direc[0]*2
        col_t = p_col + prox_direc[1]*2
        vector_fil = fil_t - self.blinky.fil
        vector_col = col_t - self.blinky.col
        return fil_t+vector_fil*2, col_t+ vector_col*2


class juego:
    def __init__(self):
        self.mapa = mapa('mapa.txt')
        self.px, self.py = self.mapa.posicion_pacman()
        self.pacman = pacman(self.px, self.py, self.mapa)
        b = blinky(self.mapa)
        i = inky(self.mapa)
        i.blinky = b
        self.fantasmas = [b, pinky(self.mapa), clyde(self.mapa), i]
        self.running = True
        self.timer = 0
        self.fase_actual = 0
        self.fases = [('scatter', 7),
                        ('chase', 20),
                        ('scatter', 7),
                        ('chase', 20),
                        ('scatter', 5),
                        ('chase', 20),
                        ('scatter', 5),
                        ('chase', 10000000000)]
    def colosiones(self):
        for fantasma in self.fantasmas:
            if self.pacman.colision(fantasma):
                if fantasma.esta_asustado:
                    self.pacman.score+=200
                    fantasma.esta_asustado = False
                    fantasma.ojos = True
                elif not fantasma.ojos:
                    self.pacman.vidas -= 1
                    if self.pacman.vidas == 0:
                        self.running = False
                    else:
                        self.posiciones_iniciales()
    def posiciones_iniciales(self):
        self.pacman.fil = self.px
        self.pacman.col = self.py
        self.pacman.x = self.pacman.col*24
        self.pacman.y = self.pacman.fil*24
        self.pacman.prox_direc = (0,0)
        self.pacman.actual_direc =(0,0)
        for fantasma in self.fantasmas:
            fantasma.fil = fantasma.fil_inicial
            fantasma.col = fantasma.col_inicial
            fantasma.x = fantasma.col*24
            fantasma.y = fantasma.fil*24
            fantasma.salio = False
    def update(self, dt):
        self.modo(dt)
        self.pacman.mover(self.pacman.fil, self.pacman.col, dt)
        self.pacman.comer(self.fantasmas)
        for fantasma in self.fantasmas:
            fantasma.mover(self.pacman.fil, self.pacman.col,self.pacman.prox_direc, dt)
        self.colosiones()
    def dibujar(self, screen):
        self.mapa.renderizar(screen)
        self.mapa.imprimir_score(self.pacman.score, screen)
        self.pacman.dibujar(screen)
        for fantasma in self.fantasmas:
            fantasma.dibujar(screen)
    def modo(self,dt):
        if self.fase_actual >= len(self.fases):
            return
        modo, tiempo = self.fases[self.fase_actual]
        for f in self.fantasmas:
            f.modo = modo
        for f in self.fantasmas:
            if f.esta_asustado:
                return
        self.timer+=dt
        if self.timer>= tiempo:
            self.timer = 0
            self.fase_actual+=1
            for f in self.fantasmas:
                f.direccion = (-f.direccion[0], -f.direccion[1])
        
        

        
            
        

        






pygame.init()
screen = pygame.display.set_mode((672, 744))
clock = pygame.time.Clock()
running = True
g = juego()

while g.running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            g.running = False
    screen.fill((0, 0, 0))
    g.dibujar(screen)
    g.update(dt)
    pygame.display.flip()






