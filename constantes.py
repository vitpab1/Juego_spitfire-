import pygame
import os
import random
pygame.mixer.init()

#defino constantes 
ANCHO = 800
ALTO = 900
WIN = pygame.display.set_mode((ANCHO, ALTO))


ENEMIGO_DEBIL = pygame.image.load(os.path.join("assets", "Aircraft_02.png"))
ENEMIGO_DIFICIL = pygame.image.load(os.path.join("assets", "Aircraft_03.png"))
ENEMIGO_INFIERNO = pygame.image.load(os.path.join("assets", "Aircraft_04.png"))

# Player player
AVION_JUGADOR = pygame.image.load(os.path.join("assets", "Aircraft_01.png"))

# Lasers
PROYECTIL_CHICO = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bullet_orange0004.png")), (25,25))
PROYECTIL_MEDIO = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bullet_orange0004.png")), (30,30))
PROYECTIL_GRANDE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bullet_orange0004.png")), (40,40))

#Disparo player
PROYECTIL_JUGADOR = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bullet_blue0004.png")), (30,30))

# Background, la "scala" a las dimensiones definidas 
FONDO_PRIMER_NIVEL = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (ANCHO, ALTO))

#Carga sonidos 
SONIDO_EXPLOSION = pygame.mixer.Sound(os.path.join("music", "explosion.wav"))
#SONIDO_DISPARO_JUGADOR = pygame.mixer.Sound(os.path.join("music", "laser.wav"))
MUSICA_JUEGO = pygame.mixer.Sound(os.path.join("music", "SONG.mp3"))
