#librerias que se usaron
import pygame
from pygame.locals import *
import time
import math
import random
import requests
import io
from urllib.request import urlopen
from math import floor

pygame.init()

# Colores
black = (0, 0, 0)
gold = (218, 165, 32)
grey = (200, 200, 200)
green = (0, 200, 0)
red = (200, 0, 0)
white = (255, 255, 255)
gold = (255, 215, 0)

# para crear la ventana del juego
ventana_ancho = 500
ventana_alto = 500

# la ventana es igual a game 
size = (ventana_ancho, ventana_alto)
ventana = pygame.display.set_mode(size)
game = pygame.display.set_mode(size)

# para que en la parte superior de la ventana salga el nombre del juego
pygame.display.set_caption("Clash Planet")

# Primero, el texto inicial:
clock = pygame.time.Clock()

# Para el texto que se meuestra en el juego,fuentes
font = pygame.image.load("font.png").convert()
font.set_colorkey((0, 0, 0))
# titulos
font2= pygame.font.Font("Tiny5-Regular.ttf", 36) 
#texto general
font3 = pygame.font.Font("Tiny5-Regular.ttf", 24) 

#para el font 1
order = ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "+", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "=", "{", "}", "[", "]", "|", "/", ":", ";", '"', "'", "<", ",", ">", ".", "?", "/", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
# Para cuando se imprima
# espacios entre las letras
spacing = 6
# Tamaño de las letras en pixeles
charsize = 8
# cuántos caracteres pueden caber en una línea antes de que el texto se "salte" a la siguiente línea
widthlmt = 16
# es un contador o índice que se utiliza para realizar un seguimiento de qué carácter del texto se está procesando y mostrando en ese momento
index = 0

#para manejar las letras de la imagen
def load_spritesheet(image, crop):
	new_image = image.subsurface(crop[0] * crop[2], crop[1] * crop[3], crop[2], crop[3])

	return new_image


# para font 1 que se usa en la introducción
def rendertext(text, pos):
	# posición inicial [0, 0]
	charpos = [0, 0]

	# calcula cuantos caracters cabe en la hoja 
	sheetwidth = (font.get_width() / charsize)
		
	#recorre los elemetos de la cadena "text"
	for char in text:	
		if char in order:
			# calcular la posición del carácter
			surf = load_spritesheet(font, (order.index(char) % sheetwidth, floor(order.index(char) / sheetwidth), charsize, charsize))
			
			#renderiza la imagen del carácter en cierta posición
			game.blit(surf, (charpos[0] + pos[0], charpos[1] + pos[1]))
			charpos[0] += spacing

		# si el carácter es un espcaio, se va a mover la posición actual
		if char == " ":
			charpos[0] += spacing

		# comprobar si el texto llegó al limite del espacio disponible, si es asi, salta una linea 
		if charpos[0] / spacing > widthlmt and char == " ":
			charpos[0] = 0
			charpos[1] += charsize + 2

# variables de texto
delaytimer = 0
delayedtext = ""
done = False
index = 0


#renderiza el tipo de texto
def rendertexttype(text, pos, delay):
	# variables
	global delaytimer, delayedtext, done, index
	#incrementa el contador cada vez que se llama la funcion
	delaytimer += 1
	if not done:
		if delay < delaytimer:
			if index < len(text):
				#reinicia el temporizador 
				delaytimer = 0
                #agrega el caracter que sigue
				delayedtext = delayedtext + text[index]
				index += 1
			else:
				done = True

	#dibuja el texto en la ventana
	rendertext(delayedtext, pos)

# por fuera del bucle principal del juego para que se muestre como la "historia"

def mostrar_intro():
    
    tiempo_inicio = pygame.time.get_ticks()  # Captura el tiempo inicial
    duracion_intro = 5000 #medido en milisegundos   50000
    
    # Para correr la pantalla
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        #saca el tiempo t5ranscurrido
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual -tiempo_inicio >= duracion_intro:
            run = False
        # Para actualizar la pantalla
        game.fill((0, 0, 20))

        rendertexttype('"Luego de que la ultima persona en la humanidad dio su ultimo respiro, dejando asi a una tierra sin vida en ella. Por esto y junto a la contaminacion se volvio loca y empezó a atacar a los demás planetas con el objetivo de ser el centro del sistema solar..."', [100, 50], 5)  
        clock.tick(60)
        
        pygame.display.update()

def dibujar_texto(texto, fuente, color, superficie, x, y):
    texto_renderizado = fuente.render(texto, True, color)
    superficie.blit(texto_renderizado, (x, y))
    
# Función para dibujar botones con bordes
def dibujar_boton(surface, boton, color_fondo, color_borde, grosor_borde):
    # Dibujar el fondo negro del botón
    pygame.draw.rect(surface, color_fondo, boton)
    # Dibujar el borde blanco
    pygame.draw.rect(surface, color_borde, boton, grosor_borde)
    
# menu inicial
def menu():
    texto = "Clash Planet"
    pos_texto = [ventana_ancho / 2 - 100, ventana_alto / 2 - 150] 
    # botones 
    boton_jugar = pygame.Rect(ventana_ancho / 2 - 100, ventana_alto / 2 - 50, 200, 50)
    boton_salir = pygame.Rect(ventana_ancho / 2 - 100, ventana_alto / 2 + 50, 200, 50)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Detectar clic en los botones
            if event.type == MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    print("Iniciar juego...")
                    game_loop()
                    
                    # Aquí puedes llamar a la función para iniciar el juego
                    return  # Salir del menú y continuar con el juego
                elif boton_salir.collidepoint(event.pos):
                    print("Salir del juego...")
                    pygame.quit()
                    exit()

        ventana.fill(black)
        dibujar_texto(texto, font2, white, ventana, pos_texto[0], pos_texto[1])

        # Dibujar botones
        dibujar_boton(ventana, boton_jugar, black, white,2)
        dibujar_boton(ventana, boton_salir, black, white, 2)

        # Dibujar texto en los botones
        dibujar_texto("Jugar", font2, white, ventana, ventana_ancho / 2 - 50, ventana_alto / 2 - 40)
        dibujar_texto("Salir", font2, white, ventana, ventana_ancho / 2 - 50, ventana_alto / 2 + 60)

        pygame.display.update()
        clock.tick(60)

# tipos de ataques:
class MoveType():
    def __init__(self, name, fuerte=None, debil=None):
        # nombre del tipo de ataque
        self.name = []
        # ataques que son más fuertes
        self.fuerte = []
        # ataques que son más débil 
        self.debil = []
    def is_effective_against(self, other_type):
        return other_type in self.fuerte # ve si es fuerte contra el otro tipo
    def is_weak_against(self, other_type):
        return other_type in self.debil  # ve si es debil

# clase para los ataques           
class Move:
    def __init__(self, name, power, move_type):
        #nombre del ataque
        self.name = name
        # daño que hace
        self.power = power
        # tipo de ataque
        self.type = move_type
# calcualr el daño que se va a hacer
    def calculate_damage(self, target_type):
        if self.type.is_effective_against(target_type):
            return self.power * 2  # Doble de daño si es efectivo
        elif self.type.is_weak_against(target_type):
            return self.power / 2  # Mitad de daño si es débil
        else:
            return self.power  # Daño normal
    def ejecutar(self, atacante, objetivo):
        print(f"{atacante.nombre} inflige {self.daño} puntos de daño a {objetivo.nombre} con {self.nombre}.")
        objetivo.recibir_daño(self.daño)

    def ejecutar(self, atacante, objetivo):
        print(f"{atacante.nombre} inflige {self.power} puntos de daño a {objetivo.nombre} con {self.name}.")
        objetivo.recibir_daño(self.calculate_damage(objetivo)) 
        
# clases de todoooo
class Habilidad:
    def __init__(self, nombre, usos=3):
        self.nombre = nombre
        self.usos_restantes = usos

    def activar(self, usuario, objetivo, ronda=None):

        if self.usos_restantes > 0:
            self.usos_restantes -= 1
            print(f"{usuario.nombre} usa {self.nombre}!")
        else:
            print(f"{self.nombre} no tiene usos restantes.")
class AtaqueRapido(Habilidad):
    def __init__(self):
        super().__init__("Ataque Rápido")

    def activar(self, usuario, objetivo, ronda=None):
        if self.usos_restantes > 0:
            super().activar(usuario, objetivo, ronda)
            daño_extra = 5  # Daño adicional de 5
            print(f"{usuario.nombre} usa {self.nombre} para realizar un ataque rápido.")

            # mensaje de daño
            print(f"{usuario.nombre} ataca a {objetivo.nombre} causando {usuario.daño_base + daño_extra} de daño (daño base: {usuario.daño_base}, extra: {daño_extra}).")

            # Realiza el ataque con el daño extra
            usuario.atacar(objetivo, daño_extra)
        else:
            print(f"{self.nombre} no tiene usos restantes.")


class DefensaTermica(Habilidad):
    def __init__(self):
        super().__init__("Defensa Térmica")

    def activar(self, usuario, objetivo, ronda=None):
        if self.usos_restantes > 0:
            self.usos_restantes -= 1
            print(f"{usuario.nombre} usa {self.nombre}. Recibirás un 20% menos de daño durante esta ronda.")

            # Activar la defensa de la Tierra
            usuario.atacar(objetivo)
            usuario.defensa_activa = True
        else:
            print(f"{self.nombre} ya no tiene usos restantes.")


class TormentaDePolvo(Habilidad):
    def __init__(self):
        super().__init__("Tormenta De Polvo")

    def activar(self, usuario, objetivo, ronda=None):
        if self.usos_restantes > 0:
            super().activar(usuario, objetivo, ronda)
            daño_extra = 10  # Daño adicional de 5
            print(f"{usuario.nombre} usa {self.nombre} para realizar un ataque rápido.")

            # Ajuste aquí para que solo se muestre un mensaje correcto
            print(f"{usuario.nombre} ataca a {objetivo.nombre} causando {usuario.daño_base + daño_extra} de daño (daño base: {usuario.daño_base}, extra: {daño_extra}).")

            # Realiza el ataque con el daño extra
            usuario.atacar(objetivo, daño_extra)
        else:
            print(f"{self.nombre} no tiene usos restantes.")

class GravedadAumentada(Habilidad):
    def __init__(self):
        super().__init__("Gravedad Aumentada")

    def activar(self, usuario, objetivo, ronda=None):
        if self.usos_restantes > 0:
            super().activar(usuario, objetivo, ronda)
            print(f"{usuario.nombre} usa {self.nombre}. ¡Aumenta el daño de los ataques en un 40% durante esta ronda!")
            usuario.daño_base = int(usuario.daño_base * 1.4)  # Aumenta el daño
            usuario.atacar(objetivo)
        else:
            print(f"{self.nombre} no tiene usos restantes.")


class AnillosDefensivos(Habilidad):
    def __init__(self):
        super().__init__("Anillos Defensivos")

    def activar(self, usuario, objetivo, ronda=None):
        if self.usos_restantes > 0:
            self.usos_restantes -= 1
            print(f"{usuario.nombre} usa {self.nombre}. Recibirás un 50% menos de daño durante esta ronda.")

            # Activar la defensa de la Tierra
            usuario.defensa2_activa = True
        else:
            print(f"{self.nombre} ya no tiene usos restantes.")

class VientoSolar(Habilidad):
    def __init__(self):
        super().__init__("Viento Solar")
    def activar(self, usuario, objetivo, ronda=None):
        if self.usos_restantes > 0:
            super().activar(usuario, objetivo, ronda)
            print(f"{usuario.nombre} usa {self.nombre}. La probabilidad de que el enemigo falle el ataque aumenta un 40%!")
            usuario.atacar(objetivo)
            objetivo.exito= 0.6  # Disminuye el éxito

        else:
            print(f"{self.nombre} no tiene usos restantes.")
            
class Tierra(pygame.sprite.Sprite):
    def __init__(self, x, y, image, vida,daño_base,level, nombre, Move):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))  
        self.rect = self.image.get_rect(center=(x, y))
        self.vida = vida
        self.vida_max = vida
        self.daño_base=daño_base
        self.defensa_activa = False
        self.habilidades = []
        self.experiencia = 0
        self.level=level
        self.nombre=nombre
        self.Move=Move

    def subir_nivel(self):
        #son 8 niveles
        if self.level<8:
            self.level+=1
            #cada vez que suba de nivle, se va a ganar una habilidad
            self.ganar_habilidad()
        else:
            print("No puedes subir de nivel, estas en el máximo")
            
    def ganar_habilidad(self):
        #dependiendo del nivel en el que esté, va ganando habilidades
        if self.level == 2:
            self.habilidades.append(ataque_rapido)
            print("Has desbloqueado la habilidad Ataque Rápido")

        elif self.level == 3:
            self.habilidades.append(defensa_termica)
            print("Has desbloqueado la habilidad Defensa Térmica")

        elif self.level == 4:
            self.habilidades.append(tormenta_polvo)
            print("Has desbloqueado la habilidad Tormenta de Polvo")
        elif self.level == 5:
            self.habilidades.append(gravedad_aumentada)
            print("Has desbloqueado la habilidad Gravedad Aumentada")
        elif self.level == 6:
            self.habilidades.append(anillos_defensas)
            print("Has desbloqueado la habilidad Anillos Defensivos")
        elif self.level == 7:
            self.habilidades.append(viento_solar)
            print("Has desbloqueado la habilidad Viento Solar")


    def atacar(self, objetivo, daño_extra=0):
        #calcular el daño total
        daño_total = self.daño_base + daño_extra
        if objetivo.defensa_activa:
            daño_total *= 0.8
            objetivo.defensa_activa = False
        objetivo.vida -= daño_total
        print(f"{self.nombre} ataca a {objetivo.nombre}, causando {daño_total} de daño.")
        if objetivo.vida <= 0:
            print(f"{objetivo.nombre} ha sido derrotado.")

    def recibir_daño(self, daño):
        self.vida -= daño
        if self.vida < 0:
            self.vida = 0 


        print(f"{self.nombre} recibió {daño:.2f} de daño. Vida restante: {self.vida:.2f}")

    def usar_habilidad(self, indice, objetivo, ronda=None):
        if 0 <= indice < len(self.habilidades):
            self.habilidades[indice].activar(self, objetivo, ronda)
        else:
            print(f"No existe la habilidad en el índice {indice}.")

    def dibujar_personaje(self, surface, scale_factor=1):
        if scale_factor != 1:
            imagen = pygame.transform.scale(self.image, (int(self.rect.width * scale_factor), int(self.rect.height * scale_factor)))
            surface.blit(imagen, self.rect)
        else:
            # si no se da un factor se dibujala imagen sin cambiar su tamaño
            surface.blit(self.image, self.rect)


    def dibujar_hp(self, surface):
        pygame.draw.rect(surface, red, (self.x - 40, self.y - 60, 80, 10))
        vida_actual = (self.vida / self.vida_max) * 80
        pygame.draw.rect(surface, gold, (self.x - 40, self.y - 60, vida_actual, 10))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, vida,daño_base,level,nombre, Move=None):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80)) 
        self.rect = self.image.get_rect(center=(x, y))
        self.vida = vida
        self.daño_base=daño_base
        self.defensa_activa = False
        self.habilidades = []
        self.level=level
        self.nombre = nombre
        self.vida_max = vida
        self.Move = Move if Move else []

    def agregar_habilidad(self, habilidad, tipo_ataque):
        habilidad.tipo_ataque = tipo_ataque
        self.habilidades.append(habilidad)

    def atacar(self, objetivo, daño_extra=0):
        daño_total = self.daño_base + daño_extra
        if objetivo.defensa_activa:
            daño_total *= 0.8
            objetivo.defensa_activa = False
        objetivo.vida -= daño_total
        print(f"{self.nombre} ataca a {objetivo.nombre}, causando {daño_total} de daño.")
        if objetivo.vida <= 0:
            print(f"{objetivo.nombre} ha sido derrotado.")

    def recibir_daño(self, daño):
        self.vida -= daño
        if self.vida < 0:
            self.vida = 0 
    
        print(f"{self.nombre} recibió {daño:.2f} de daño. Vida restante: {self.vida:.2f}")

    def usar_habilidad(self, indice, objetivo, ronda=None):
        if 0 <= indice < len(self.habilidades):
            self.habilidades[indice].activar(self, objetivo, ronda)
        else:
            print(f"No existe la habilidad en el índice {indice}.")
            
    def dibujar_personaje(self, surface, scale_factor=1):
            # Si se proporciona un factor de escala, redimensionamos la imagen
        if scale_factor != 1:
            imagen = pygame.transform.scale(self.image, (int(self.rect.width * scale_factor), int(self.rect.height * scale_factor)))
            surface.blit(imagen, self.rect)
        else:
            # Si no se da  el factor, se dibuja la imagen sin cambiar su tamaño
            surface.blit(self.image, self.rect)

    def dibujar_hp(self, surface):
        # fondo de barra
        pygame.draw.rect(surface, red,(self.x - 40, self.y - 60, 80, 10))
        #calcular vida
        vida_actual = (self.vida / self.vida_max) * 80
        #barra
        pygame.draw.rect(surface, gold, (self.x - 40, self.y - 60, vida_actual, 10))


#mas funciones que se usan en el loop principal

#crar botones
def create_button(screen, font, color, hover_color, width, height, left, top, text_color, label):
    mouse_cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #donde va a estar el boton 
    button = pygame.Rect(left, top, width, height)

    if button.collidepoint(mouse_cursor):
        pygame.draw.rect(screen, hover_color, button)
        if click[0]:
            return True
    else:
        pygame.draw.rect(screen, color, button)

    text = font3.render(label, True, text_color)
    text_rect = text.get_rect(center=button.center)
    screen.blit(text, text_rect)

    return False
# para los mensajes dentro del juego       
def display_message(message):

    # dibuja el cuadrado deonde va a estar el mensaje
    pygame.draw.rect(game, white, (10, 350, 480, 140))
    pygame.draw.rect(game, white, (10, 350, 480, 140), 3)

    # mostrar en la ventana
    text = font3.render(message, True, white)
    text_rect = text.get_rect()
    text_rect.x = 30
    text_rect.y = 410
    game.blit(text, text_rect)

    pygame.display.update()
    
def mostrar_nivel_subido():
    ventana.fill((0, 0, 0))  # Fondo negro
    
    # Dibujar el texto en el centro
    texto = f"¡Has subido de nivel! Ahora eres nivel {tierra.level}"
    # calcula el tamaño del texto
    texto_width, texto_height = font3.size(texto)

    texto_x = (ventana_ancho - texto_width) // 2  # centrar en el eje x(horizontal)
    texto_y = 50  # margen
    dibujar_texto(texto, font3, white, ventana, texto_x, texto_y)
    
    # Botones de "jugar" y "salir"
    #tamaño de botones
    button_width, button_height = 150, 40  
    margen_x = (ventana_ancho - button_width * 2 - 20) // 2  # Centrar en el eje x
    margen_y = ventana_alto - 100  # ajuste de posición en el eje y
    #espacio entre los botones
    spacing_x = 20  

    # posición de los botones "salir" y "seguir jugando"
    button_positions = [
        (margen_x, margen_y),  # boton para seguir jugando
        (margen_x + button_width + spacing_x, margen_y)  # botón para dejar de jugar "Salir"
    ]

    # para que los botones estén centrados
    for i, (pos_x, pos_y) in enumerate(button_positions):
        if create_button(ventana, font3, white, grey, button_width, button_height, pos_x, pos_y, black, ["Seguir jugando", "Salir"][i]):
            if i == 0:  # "Seguir jugando"
                return "continue"
            elif i == 1:  # "Salir"
                return "exit"

    pygame.display.update()
    clock.tick(60)

#pantalla para cuando se termina la batalla
def mostrar_game_over():
    # cambia el fondo a rojo, rojo=(255,0,0)
    ventana.fill((255, 0, 0)) 
    
    # dibuja "Game Over" centrado
    texto = "Game Over"
    # calcula el tamaño del texto para poder centrarlo
    texto_width, texto_height = font2.size(texto)
    texto_x = (ventana_ancho - texto_width) // 2  
    texto_y = (ventana_alto - texto_height) // 2 - 50  
    dibujar_texto(texto, font2, white, ventana, texto_x, texto_y)
    
    # posición de los botones "Seguir intentándolo" y "Salir"
    button_width, button_height = 200, 50
    margen_x = (ventana_ancho - button_width) // 2
    margen_y = ventana_alto - 150  
    spacing_x = 20

    # posicion de  botones
    button_positions = [
        (margen_x, margen_y),  # boton de "Seguir intentándolo"
        (margen_x + button_width + spacing_x, margen_y)  # boton para "Salir"
    ]

    # dibuja los botones 
    for i, (pos_x, pos_y) in enumerate(button_positions):
        if create_button(ventana, font3, white, grey, button_width, button_height, pos_x, pos_y, black, ["Seguir intentándolo", "Salir"][i]):
            #seguir intentando
            if i == 0:  
                return "continue"
            #salir
            elif i == 1:  
                return "exit"

    pygame.display.update()
    clock.tick(60)
    
#llamar a la funcion movetype
ataq_normal = MoveType(name="normal")
ataq_habilidad = MoveType(name="habilidad")

#establecer las relaciones de fortalezas y debilidades
ataq_normal.fuerte = []  
#debil contra "habilida"
ataq_normal.debil = [ataq_habilidad]  
#fuerte contra "normal"
ataq_habilidad.fuerte = [ataq_normal]  
ataq_habilidad.debil = []  

# dos tipos de ataques = normal y habilidades
# ataques normales y predeterminados
golpe_terrestre = Move("Golpe Terrestre", 15, ataq_normal)
golpe_mar = Move("Lluvia marina", 10, ataq_normal)
rafaga_piedra = Move("Ráfaga de Piedra", 20, ataq_normal)
golpe_contaminacion = Move("Golpe contaminación", 30, ataq_normal)
movimientos = [golpe_terrestre,rafaga_piedra, golpe_mar, golpe_contaminacion]

#Crear objetos
# personaje principal, tierra
tierra = Tierra(400,500, "tierra.png",vida=100,daño_base=10,level=1,nombre="tierra",Move=movimientos)
#enemigos
enemys = [ 
    Enemy(400, 150, "mercurio.png", vida=50, daño_base=8,level=1,nombre="mercurio"),
    Enemy(400, 150, "venus.png", vida=70, daño_base=10,level=2,nombre="venus"),
    Enemy(400, 150, "marte.png", vida=90, daño_base=10,level=3,nombre="marte"),
    Enemy(400, 150, "jupiter.png", vida=95, daño_base=12,level=4, nombre="jupiter"),
    Enemy(400, 150, "saturno.png", vida=105, daño_base=15,level=5,nombre="saturno"),
    Enemy(400, 150, "urano.png", vida=105, daño_base=15,level=6, nombre="urano"),
    Enemy(400, 150, "neptuno.png", vida=105, daño_base=15,level=7, nombre="neptuno"),
    Enemy(400, 150, "sol.png", vida=115, daño_base=30,level=8, nombre="sol") #poner esto en los niveles
]
#determinar los enemigos    
mercurio = enemys[0]
venus = enemys[1]
marte = enemys[2]
jupiter = enemys[3]
saturno = enemys[4]
urano = enemys[5]
neptuno = enemys[6]
sol = enemys[7]

#habilidades
ataque_rapido=AtaqueRapido()
defensa_termica=DefensaTermica()
tormenta_polvo=TormentaDePolvo()
gravedad_aumentada=GravedadAumentada()
anillos_defensas=AnillosDefensivos()
viento_solar=VientoSolar()

#se asigna habilidades
mercurio.agregar_habilidad(ataque_rapido, ataq_habilidad)
venus.agregar_habilidad(defensa_termica, ataq_habilidad)
marte.agregar_habilidad(tormenta_polvo, ataq_habilidad)
jupiter.agregar_habilidad(gravedad_aumentada, ataq_habilidad)
saturno.agregar_habilidad(anillos_defensas, ataq_habilidad)
urano.agregar_habilidad(viento_solar, ataq_habilidad)

#asignar ataques y habilidades
for enemy, habilidad in zip(enemys, [ataque_rapido, defensa_termica, tormenta_polvo, gravedad_aumentada, anillos_defensas, viento_solar]):
    #agregar habilidad
    enemy.agregar_habilidad(habilidad, ataq_habilidad) 
    #seleccionar 2 ataques normales
    enemy.Move = random.sample(tierra.Move[:4], 2)  
    enemy.Move.append(habilidad)


#loop principal 
def game_loop():
    global tierra, enemys

    print("Iniciando el juego...")
    
    game_status = 'select rival'
    selected_enemy = None
    #controla si el bucle se está ejecutando
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            #detecta el click izquierdo
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()
                for enemy in enemys:
                    #si hace click izuierdo en uno de los enemigos, este se selecciona
                    if enemy.rect.collidepoint(mouse_pos) and enemy.vida > 0:
                        selected_enemy = enemy
                        #cambia el estado del juego a "battle"
                        game_status = 'battle'

        #dibujar la pantalla
        ventana.fill(black)

        if game_status == 'select rival':
            #dinuja texto para indicar que hay que seleccionar al enemigo
            dibujar_texto("Selecciona tu enemigo", font2, white, ventana, 100, 30)
            #dibuja los enemigos en la pantalla
            for idx, enemy in enumerate(enemys):
                row = idx // 3  #fila
                col = idx % 3   #columna
                
                #ajuste para que los enemigos estén en dibujados en filas y colunas
                #espacio entre enemigos
                enemy.x = 95 + col * 150  
                #primera fial
                if row == 0: 
                    enemy.y = 150
                #segunda fila
                elif row == 1:  
                    enemy.y = 300
                #tercera fila
                else:  
                    enemy.y = 450
                enemy.rect.center = (enemy.x, enemy.y)
                enemy.dibujar_personaje(ventana)
                
        # si el estatus del juego es "battle"
        elif game_status == 'battle' and selected_enemy is not None:
            #configura la posición de los personajes y bibuja la barra de vida
            #ubicación de la tierra
            tierra.x = 100  # se ubibicac a la derecha
            tierra.y = 230  # Centrado verticalmente
            tierra.rect.center = (tierra.x, tierra.y)
            tierra.dibujar_personaje(ventana, scale_factor=2) 
            #ubicación enemigo
            selected_enemy.x = 350  # se ubica a la izquierda
            selected_enemy.y = 150 # Centrado verticalmente
            selected_enemy.rect.center = (selected_enemy.x, selected_enemy.y)
            selected_enemy.dibujar_personaje(ventana, scale_factor=2)  # hace más grande la imagen del enemigo

            # Dibuja barras de vida
            tierra.dibujar_hp(ventana)
            selected_enemy.dibujar_hp(ventana)

            pygame.display.update()
            #clock.tick(60)
            
            #cambia el modo del juego 
            game_status = "player turn"

        #turno del jugador
        elif game_status == "player turn":
            #fondo negro
            ventana.fill((0, 0, 0))  
            dibujar_texto(f"Batalla contra {selected_enemy.nombre}", font2, white, ventana,70,30)

            tierra.dibujar_personaje(ventana,scale_factor=2)
            selected_enemy.dibujar_personaje(ventana, scale_factor=2)
            tierra.dibujar_hp(ventana)
            selected_enemy.dibujar_hp(ventana)
            # losprimeros 4 movimientos de la Tierra
            ataques = tierra.Move[:4]
            # configuración para la cuadrícula de botones
            button_width, button_height = 200, 50
            margen_x = 50
            margen_y = ventana_alto - 150 
            spacing_x = 20 # espacio entre botones
            button_positions = [
                (margen_x, margen_y),  # boton fila superior izquierda
                (margen_x + button_width + spacing_x, margen_y),  # boton fila superior derecha
                (margen_x, margen_y + button_height + 10),  # boton fila inferior izquierda
                (margen_x + button_width + spacing_x, margen_y + button_height + 10)  # boton fila inferior derecha
            ]
                    # dibuja los botones de ataque 
            for i, (pos_x, pos_y) in enumerate(button_positions):
                #solo se muestra si hay movimiento disponibles
                if i < len(ataques):  
                    ataque = ataques[i]
                    if create_button(ventana, font3, white, grey, button_width, button_height, pos_x, pos_y, black, ataque.name):
                        daño = ataque.calculate_damage(selected_enemy)
                        selected_enemy.recibir_daño(daño)
                        print(f"{tierra.nombre} usa {ataque.name}")

                        # verifica si se derrotó al enemigo
                        if selected_enemy.vida <= 0:
                            selected_enemy.vida = 0  # se asegura que la vida no sea negativa
                            #se llama a lafuncion de la clase Tierra para subir de nivel
                            tierra.subir_nivel()
                            game_status = "level up"  # Cambiar a la fase de nivelación}
                            selected_enemy=None



            pygame.display.update()
            clock.tick(60)
        #turno del enemigo
        elif game_status == "rival turn":
            ventana.fill((0, 0, 0))  # Fondo negro
            tierra.dibujar_personaje(ventana,scale_factor=2)
            selected_enemy.dibujar_personaje(ventana,scale_factor=2)
            tierra.dibujar_hp(ventana)
            selected_enemy.dibujar_hp(ventana)

            display_message("El enemigo está atacando...")
            time.sleep(2)
            #elegir aleatoriamente un ataque del enemigo
            ataque = random.choice(selected_enemy.Move) 

            #si es un ataque normal
            if isinstance(ataque, Move):  
                daño = ataque.calculate_damage(tierra)
                tierra.recibir_daño(daño)
                print(f"{selected_enemy.nombre} usa {ataque.name} causando {daño} de daño.")
            #si es una habilidad
            elif isinstance(ataque, Habilidad): 
                ataque.activar(selected_enemy, tierra)
                

            pygame.display.update()
            #si la tierra se queda sin vida, se acaba el juego 
            if tierra.vida <= 0:
                game_status = "game over"
            #si sigue con vida, es turno del jugador 
            else:
                game_status = "player turn"
            pygame.display.update()

        #subir nivel
        elif game_status == "level up":
            #muestra el mensaje
            resultado = mostrar_nivel_subido()  
            if resultado == "exit":
                #salir del juego 
                running = False 
            #seguir jugando
            elif resultado == "continue":
                game_status = "select rival" 
        #si el juevo finaliza 
        elif game_status == "game over":
            #llama  a lafuncion que dibuja que se terminó el juego
            resultado = mostrar_game_over()  
            if resultado == "exit":
                #salir del juego
                running = False  

            #continuar jugando, se reinicia todo
            elif resultado == "continue":
                tierra.vida = tierra.vida_maxima  #reinicia la vida
                #resetea el nivel
                tierra.level = 1 

                game_status = "select rival"
                
        pygame.display.update()
        clock.tick(60)
# script, para mostrar el juego
def main():
    mostrar_intro()
    menu()
    pygame.quit()
    exit()  # Esto asegura que el juego termine correctamente

if __name__ == "__main__":
    main()  # Luego pasa al juego principal
pygame.quit()