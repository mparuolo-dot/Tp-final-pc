import pygame
import math
import random

# --- CONFIGURACIÓN Y PALETA ---
paleta_colores = {
    "X" : (0, 0, 150),        # Paredes (Azul para que se vea mejor)
    "." : (255, 255, 255),    # Comida pequeña
    " " : (0, 0, 0),          # Fondo negro
    "G" : (0, 0, 0),          # Casa de fantasmas
    "-" : (255, 255, 0),      # Puerta casa
    "o" : (255, 255, 255),    # Power Pellet
    "P" : (0, 0, 0),          # Inicio Pacman
    "T" : (0, 0, 0)           # Túnel
}

largo_fila = 28
alto_mapa = 31
tamaño_pixel = 20
tamaño_score = 60

# --- CLASES ---

class Personajes:   
    """ Clase base para todos los personajes """
    def __init__(self, mapa, pantalla):
        self.mapa = mapa  
        self.pantalla = pantalla

class Pacman(Personajes): 
    def __init__(self, x: int, y: int, mapa, pantalla):
        Personajes.__init__(self, mapa , pantalla)
        # Seteamos posición inicial en píxeles
        self.x = x * tamaño_pixel   
        self.y = y * tamaño_pixel    
        self.power_pellet = False  
        self.tiempo_de_power_pellet = 0 
        self.direccion = ""  
        self.proxima_direccion = ""  
        
        # Intentamos cargar imágenes (si no están, el juego fallará, asegúrate de tener los .png)
        try:
            self.pacman_boca_cerrada = pygame.transform.scale(pygame.image.load("boca_cerrada.png"), (tamaño_pixel, tamaño_pixel))
            self.pacman_boca_abierta = pygame.transform.scale(pygame.image.load("boca_abierta.png"), (tamaño_pixel, tamaño_pixel))
            self.pacman_boca_cerrada_parcial = pygame.transform.scale(pygame.image.load("boca_semiabierta.png"), (tamaño_pixel, tamaño_pixel))
        except:
            # Fallback por si no hay imágenes (un círculo amarillo)
            self.pacman_boca_abierta = pygame.Surface((tamaño_pixel, tamaño_pixel))
            self.pacman_boca_abierta.fill((255, 255, 0))
            self.pacman_boca_cerrada = self.pacman_boca_abierta
            self.pacman_boca_cerrada_parcial = self.pacman_boca_abierta

        self.contador_fps_dibujo = 0
        self.mostrar_pacman = self.pacman_boca_abierta
        self.direccion_para_imagen = "derecha"
        self.rotacion = 0
    
    def mover(self, velocidad: int, dt: float):
        claves = pygame.key.get_pressed()         
        velocidad_tiles = 1 
        velocidad_pixeles = velocidad * 60
        
        # Lectura de inputs
        if claves[pygame.K_LEFT]:
            self.proxima_direccion = "izquierda" 
        elif claves[pygame.K_RIGHT]:
            self.proxima_direccion = "derecha" 
        elif claves[pygame.K_UP]:                       
            self.proxima_direccion = "arriba"
        elif claves[pygame.K_DOWN]:
            self.proxima_direccion = "abajo"

        # Lógica de doblar (solo cuando está centrado en un tile)
        if self.x % tamaño_pixel < velocidad_pixeles * dt and self.y % tamaño_pixel < velocidad_pixeles * dt:
            self.x = int(self.x // tamaño_pixel) * tamaño_pixel
            self.y = int(self.y // tamaño_pixel) * tamaño_pixel  
            
            tile_x = self.x // tamaño_pixel
            tile_y = self.y // tamaño_pixel

            # Probar si puede doblar a la dirección deseada
            proxima_x, proxima_y = tile_x, tile_y
            if self.proxima_direccion == "izquierda": proxima_x -= velocidad_tiles
            elif self.proxima_direccion == "derecha": proxima_x += velocidad_tiles
            elif self.proxima_direccion == "arriba": proxima_y -= velocidad_tiles
            elif self.proxima_direccion == "abajo": proxima_y += velocidad_tiles

            # Si no hay pared en la dirección deseada, doblamos
            if self.mapa[proxima_y][proxima_x % largo_fila] != "X":
                self.direccion = self.proxima_direccion

            # Verificar si chocamos de frente en la dirección actual
            adelante_x, adelante_y = tile_x, tile_y
            if self.direccion == "izquierda": adelante_x -= velocidad_tiles
            elif self.direccion == "derecha": adelante_x += velocidad_tiles
            elif self.direccion == "arriba": adelante_y -= velocidad_tiles
            elif self.direccion == "abajo": adelante_y += velocidad_tiles

            if self.mapa[adelante_y][adelante_x % largo_fila] == "X":
                self.direccion = ""

        # Aplicar movimiento
        if self.direccion == "izquierda":
            self.x -= velocidad_pixeles * dt
            self.direccion_para_imagen = "izquierda"
        elif self.direccion == "derecha":
            self.x += velocidad_pixeles * dt
            self.direccion_para_imagen = "derecha"
        elif self.direccion == "arriba":
            self.y -= velocidad_pixeles * dt   
            self.direccion_para_imagen = "arriba"
        elif self.direccion == "abajo":
            self.y += velocidad_pixeles * dt
            self.direccion_para_imagen = "abajo"

        # Teletransporte túnel
        if self.x < 0:
            self.x = (largo_fila - 1) * tamaño_pixel
        elif self.x > (largo_fila - 1) * tamaño_pixel:
            self.x = 0

    def comer(self) -> int: 
        if self.x % tamaño_pixel < 8 and self.y % tamaño_pixel < 8:
            fila = int(self.y // tamaño_pixel)
            columna = int(self.x // tamaño_pixel)
            
            char = self.mapa[fila][columna]
            if char == ".":
                self.mapa[fila][columna] = " "
                return 10
            elif char == "o":
                self.mapa[fila][columna] = " "
                self.power_pellet = True
                self.tiempo_de_power_pellet = 480 # Aumentamos tiempo (8 segundos aprox)
                return 50
        return 0
            
    def ver_power_pellet(self) -> bool:
        if self.tiempo_de_power_pellet > 0:
            self.tiempo_de_power_pellet -= 1
            self.power_pellet = True
            return True
        else:
            self.power_pellet = False 
            return False
        
    def dibujar(self, dt):
        self.contador_fps_dibujo += 1
        if self.contador_fps_dibujo >= 60:
            self.contador_fps_dibujo = 0
            
        # Animación básica de boca
        if self.contador_fps_dibujo < 20:
            self.mostrar_pacman = self.pacman_boca_abierta
        elif self.contador_fps_dibujo < 40:
            self.mostrar_pacman = self.pacman_boca_cerrada_parcial
        else:
            self.mostrar_pacman = self.pacman_boca_cerrada

        # Rotación según dirección
        img_a_dibujar = self.mostrar_pacman
        if self.direccion_para_imagen == "arriba":
            img_a_dibujar = pygame.transform.rotate(self.mostrar_pacman, 90)
        elif self.direccion_para_imagen == "abajo":
            img_a_dibujar = pygame.transform.rotate(self.mostrar_pacman, 270)
        elif self.direccion_para_imagen == "izquierda":
            img_a_dibujar = pygame.transform.flip(self.mostrar_pacman, True, False)
        
        self.pantalla.blit(img_a_dibujar, (int(self.x), int(self.y) + tamaño_score - 10))

class Fantasma(Personajes):
    def __init__(self, x, y, mapa, pantalla, color, nombre, esquina_nombre):
        Personajes.__init__(self, mapa, pantalla)
        self.x = x * tamaño_pixel
        self.y = y * tamaño_pixel
        self.color = color
        self.nombre = nombre
        self.direccion = "arriba"
        self.velocidad = 1.8
        self.frightened = False
        
        # Definimos las coordenadas de las esquinas del mapa para el modo dispersión
        self.objetivos_esquinas = {
            "Arriba Izquierda": (1, 1),
            "Arriba Derecha": (largo_fila - 2, 1),
            "Abajo Izquierda": (1, alto_mapa - 2),
            "Abajo Derecha": (largo_fila - 2, alto_mapa - 2)
        }
        self.esquina_objetivo = self.objetivos_esquinas[esquina_nombre]

    def mover(self, pacman_x, pacman_y, power_pellet_activo, dt):
        # Ajustamos velocidad si está asustado
        v_actual = self.velocidad
        if power_pellet_activo:
            v_actual = 1.0
            self.frightened = True
        else:
            self.frightened = False

        velocidad_pixeles = v_actual * 60 * dt

        # Solo decide dirección cuando está centrado en el tile
        if self.x % tamaño_pixel == 0 and self.y % tamaño_pixel == 0:
            fila = int(self.y // tamaño_pixel)
            col = int(self.x // tamaño_pixel)

            # El objetivo cambia según el estado
            if power_pellet_activo:
                # Objetivo aleatorio
                target_x, target_y = random.randint(0, largo_fila), random.randint(0, alto_mapa)
            else:
                # Alternar entre perseguir a Pacman y su esquina (simple)
                if random.random() > 0.8: # 20% del tiempo va a su esquina
                    target_x, target_y = self.esquina_objetivo
                else:
                    target_x, target_y = pacman_x // tamaño_pixel, pacman_y // tamaño_pixel

            posibles_direcciones = []
            # Chequeamos las 4 direcciones (evitando volver atrás)
            direcciones = [
                ("arriba", 0, -1, "abajo"),
                ("abajo", 0, 1, "arriba"),
                ("izquierda", -1, 0, "derecha"),
                ("derecha", 1, 0, "izquierda")
            ]

            for nombre_dir, dx, dy, opuesta in direcciones:
                if self.direccion != opuesta: # No puede dar la vuelta 180°
                    nx, ny = col + dx, fila + dy
                    if 0 <= ny < alto_mapa and self.mapa[ny][nx % largo_fila] != "X":
                        distancia = math.sqrt((nx - target_x)**2 + (ny - target_y)**2)
                        posibles_direcciones.append((nombre_dir, distancia))

            if posibles_direcciones:
                # Elegimos la que tenga menor distancia al objetivo
                posibles_direcciones.sort(key=lambda x: x[1])
                self.direccion = posibles_direcciones[0][0]

        # Movimiento físico
        if self.direccion == "arriba": self.y -= velocidad_pixeles
        elif self.direccion == "abajo": self.y += velocidad_pixeles
        elif self.direccion == "izquierda": self.x -= velocidad_pixeles
        elif self.direccion == "derecha": self.x += velocidad_pixeles

        # Túnel
        if self.x < 0: self.x = (largo_fila - 1) * tamaño_pixel
        elif self.x > (largo_fila - 1) * tamaño_pixel: self.x = 0

    def dibujar(self):
        # Si está asustado es azul, si no su color original
        color_cuerpo = (0, 0, 255) if self.frightened else self.color
        
        pos_y_ajustada = int(self.y) + tamaño_score - 10
        # Dibujamos un círculo con "patitas" (rectángulo abajo)
        pygame.draw.circle(self.pantalla, color_cuerpo, (int(self.x) + 10, pos_y_ajustada + 10), 9)
        pygame.draw.rect(self.pantalla, color_cuerpo, (int(self.x) + 1, pos_y_ajustada + 10, 18, 9))
        
        # Ojos
        pygame.draw.circle(self.pantalla, (255, 255, 255), (int(self.x) + 6, pos_y_ajustada + 7), 3)
        pygame.draw.circle(self.pantalla, (255, 255, 255), (int(self.x) + 14, pos_y_ajustada + 7), 3)

class Puntaje:
    def __init__(self, score: int, pantalla):
        self.pantalla = pantalla
        self.puntos = score
        self.high_score = self.cargar_high_score()
        self.vidas = 3
        self.lvl = 1

    def cargar_high_score(self) -> int: 
        try:
            with open("high_score.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def actualizar_high_score(self):
        with open("high_score.txt", "w") as f:
            f.write(str(self.high_score))

    def actualizar_puntaje(self, score: int):
        self.puntos += score
        if self.puntos > self.high_score:
            self.high_score = self.puntos
        return self.puntos

    def actualizar_lvl(self, lvl: int):
        self.lvl += lvl

    def mostrar(self):
        fuente = pygame.font.SysFont("Courier", 35)
        fuente_p = pygame.font.SysFont("Courier", 18)
        
        txt_score = fuente.render(f"SCORE: {self.puntos}", True, (255, 255, 255))
        txt_high = fuente.render(f"HIGH: {self.high_score}", True, (255, 255, 0))
        txt_lvl = fuente_p.render(f"LEVEL: {self.lvl}", True, (255, 255, 255))
        
        self.pantalla.blit(txt_score, (20, 10))
        self.pantalla.blit(txt_high, (250, 10))
        self.pantalla.blit(txt_lvl, (480, 25))

        # Dibujar vidas abajo
        for i in range(self.vidas):
            pygame.draw.circle(self.pantalla, (255, 217, 0), (30 + (i * 30), 710), 10)

class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((largo_fila * tamaño_pixel, (alto_mapa * tamaño_pixel) + tamaño_score + 50))
        pygame.display.set_caption("Pac-Man TP Final")
        self.fps = pygame.time.Clock()
        self.puntaje = Puntaje(0, self.pantalla)
        
        self.estado = "Inicio"
        self.mostrar_enter = True
        self.timer_texto = 0
        
        # Datos de fantasmas posibles
        self.info_fantasmas = [
            {"nombre": "Blinky", "color": (255, 0, 0), "desc": "Rojo - Perseguidor"},
            {"nombre": "Pinky", "color": (255, 182, 193), "desc": "Rosa - Emboscador"},
            {"nombre": "Inky", "color": (0, 255, 255), "desc": "Celeste - Flanqueador"},
            {"nombre": "Clyde", "color": (255, 165, 0), "desc": "Naranja - Tímido"},
            {"nombre": "Spike", "color": (0, 255, 0), "desc": "Verde - Interceptor"},
            {"nombre": "Coward", "color": (128, 0, 128), "desc": "Violeta - Cobarde"}
        ]
        
        self.seleccionados = [] # Índices (1-6)
        self.config_esquinas = [] # Lista de dicts con nombre y esquina
        self.paso_esquinas = 0
        self.objetos_fantasmas = []
        
        self.empezar_mapa()

    def empezar_mapa(self):
        self.mapa = []
        self.comida_faltante = 0
        with open("mapa.txt", "r") as f:
            for linea in f:
                self.mapa.append(list(linea.strip()))

        pos_x, pos_y = 1, 1
        self.pos_spawn_fantasmas = (13, 14) # Default centro casa
        
        for f in range(alto_mapa):
            for c in range(largo_fila):
                if self.mapa[f][c] == "P":
                    pos_x, pos_y = c, f
                elif self.mapa[f][c] == "G":
                    self.pos_spawn_fantasmas = (c, f)
                elif self.mapa[f][c] in [".", "o"]:
                    self.comida_faltante += 1
        
        self.pacman = Pacman(pos_x, pos_y, self.mapa, self.pantalla)
        
        # Solo creamos fantasmas si ya pasamos la configuración
        if self.estado == "Juego":
            self.crear_fantasmas()

    def crear_fantasmas(self):
        self.objetos_fantasmas = []
        for i in range(len(self.seleccionados)):
            idx = self.seleccionados[i] - 1
            datos = self.info_fantasmas[idx]
            esquina = self.config_esquinas[i]["esquina"]
            
            nuevo_f = Fantasma(
                self.pos_spawn_fantasmas[0], 
                self.pos_spawn_fantasmas[1],
                self.mapa, self.pantalla,
                datos["color"], datos["nombre"], esquina
            )
            self.objetos_fantasmas.append(nuevo_f)

    def pantalla_inicio(self):
        self.pantalla.fill((0, 0, 0))
        f_titulo = pygame.font.SysFont("Courier", 60, bold=True)
        f_sub = pygame.font.SysFont("Courier", 25)
        
        self.pantalla.blit(f_titulo.render("PAC-MAN", True, (255, 255, 0)), (150, 150))
        
        self.timer_texto += 1
        if self.timer_texto % 60 < 30:
            msg = f_sub.render("PRESIONE ENTER PARA EMPEZAR", True, (255, 255, 255))
            self.pantalla.blit(msg, (70, 400))
            
        pygame.display.flip()

    def menu_eleccion(self):
        self.pantalla.fill((0, 0, 0))
        fuente = pygame.font.SysFont("Courier", 22)
        
        self.pantalla.blit(fuente.render(f"Elegí 4 Fantasmas ({len(self.seleccionados)}/4)", True, (255, 255, 255)), (50, 50))
        
        for i in range(len(self.info_fantasmas)):
            color = self.info_fantasmas[i]["color"]
            nombre = self.info_fantasmas[i]["nombre"]
            desc = self.info_fantasmas[i]["desc"]
            
            # Si está seleccionado, dibujar un recuadro
            if (i + 1) in self.seleccionados:
                pygame.draw.rect(self.pantalla, (255, 255, 255), (40, 100 + (i*50), 480, 45), 2)
                
            self.pantalla.blit(fuente.render(f"{i+1}. {nombre}", True, color), (60, 110 + (i*50)))
            self.pantalla.blit(fuente.render(desc, True, (150, 150, 150)), (200, 110 + (i*50)))

        if len(self.seleccionados) == 4:
            self.pantalla.blit(fuente.render("PRESIONA ENTER PARA CONTINUAR", True, (255, 255, 0)), (80, 500))

        pygame.display.flip()

    def menu_esquinas(self):
        self.pantalla.fill((0, 0, 0))
        fuente = pygame.font.SysFont("Courier", 25)
        
        # Cuál fantasma estamos configurando
        indice_f = self.seleccionados[self.paso_esquinas] - 1
        datos = self.info_fantasmas[indice_f]
        
        self.pantalla.blit(fuente.render(f"Esquina para: {datos['nombre']}", True, datos["color"]), (50, 100))
        
        opciones = ["1. Arriba Izquierda", "2. Arriba Derecha", "3. Abajo Izquierda", "4. Abajo Derecha"]
        for i in range(4):
            self.pantalla.blit(fuente.render(opciones[i], True, (255, 255, 255)), (100, 200 + (i*60)))
            
        pygame.display.flip()

    def bucle_principal(self):
        running = True
        while running:
            dt = self.fps.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if self.estado == "Inicio" and event.key == pygame.K_RETURN:
                        self.estado = "Eleccion"
                    
                    elif self.estado == "Eleccion":
                        if pygame.K_1 <= event.key <= pygame.K_6:
                            num = event.key - pygame.K_0
                            if num not in self.seleccionados and len(self.seleccionados) < 4:
                                self.seleccionados.append(num)
                        if event.key == pygame.K_RETURN and len(self.seleccionados) == 4:
                            self.estado = "Esquinas"
                    
                    elif self.estado == "Esquinas":
                        if pygame.K_1 <= event.key <= pygame.K_4:
                            opciones = ["Arriba Izquierda", "Arriba Derecha", "Abajo Izquierda", "Abajo Derecha"]
                            esq = opciones[event.key - pygame.K_1]
                            self.config_esquinas.append({"esquina": esq})
                            self.paso_esquinas += 1
                            if self.paso_esquinas == 4:
                                self.estado = "Juego"
                                self.crear_fantasmas()

            if self.estado == "Inicio":
                self.pantalla_inicio()
            elif self.estado == "Eleccion":
                self.menu_eleccion()
            elif self.estado == "Esquinas":
                self.menu_esquinas()
            elif self.estado == "Juego":
                self.dibujar_escena(dt)
                
        self.puntaje.actualizar_high_score()
        pygame.quit()

    def dibujar_escena(self, dt):
        self.pantalla.fill((0, 0, 0))
        
        # Dibujar Mapa
        for f in range(alto_mapa):
            for c in range(largo_fila):
                char = self.mapa[f][c]
                color = paleta_colores.get(char, (0, 0, 0))
                rect = (c * tamaño_pixel, f * tamaño_pixel + tamaño_score - 10, tamaño_pixel, tamaño_pixel)
                
                if char == ".":
                    pygame.draw.circle(self.pantalla, color, (rect[0] + 10, rect[1] + 10), 2)
                elif char == "o":
                    pygame.draw.circle(self.pantalla, color, (rect[0] + 10, rect[1] + 10), 5)
                elif char == "X":
                    pygame.draw.rect(self.pantalla, color, rect)
                elif char == "-":
                    pygame.draw.rect(self.pantalla, (200, 200, 200), rect)

        # Lógica Pacman
        power_activo = self.pacman.ver_power_pellet()
        vel_p = 2.2 if power_activo else 2.0
        self.pacman.mover(vel_p, dt)
        
        puntos = self.pacman.comer()
        if puntos > 0:
            self.puntaje.actualizar_puntaje(puntos)
            self.comida_faltante -= 1
            if self.comida_faltante <= 0:
                self.puntaje.actualizar_lvl(1)
                self.empezar_mapa()

        self.pacman.dibujar(dt)

        # Lógica Fantasmas
        for g in self.objetos_fantasmas:
            g.mover(self.pacman.x, self.pacman.y, power_activo, dt)
            g.dibujar()
            
            # Colisión
            distancia = math.sqrt((self.pacman.x - g.x)**2 + (self.pacman.y - g.y)**2)
            if distancia < 15:
                if power_activo:
                    # Fantasma vuelve a casa
                    g.x, g.y = self.pos_spawn_fantasmas[0]*tamaño_pixel, self.pos_spawn_fantasmas[1]*tamaño_pixel
                    self.puntaje.actualizar_puntaje(200)
                else:
                    self.puntaje.vidas -= 1
                    if self.puntaje.vidas <= 0:
                        self.estado = "Inicio" # Game over simple
                        self.puntaje.vidas = 3
                        self.puntaje.puntos = 0
                        self.empezar_mapa()
                    else:
                        # Reset posición
                        self.pacman.x = 1 * tamaño_pixel # Ejemplo reset manual
                        self.pacman.y = 1 * tamaño_pixel
                        for ghost in self.objetos_fantasmas:
                            ghost.x, ghost.y = self.pos_spawn_fantasmas[0]*tamaño_pixel, self.pos_spawn_fantasmas[1]*tamaño_pixel

        self.puntaje.mostrar()
        pygame.display.flip()

game = Juego()
game.bucle_principal()