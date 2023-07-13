import pygame

import constantes

pygame.font.init() 
pygame.mixer.init()

class Proyectil:
    #init permite inicializar los atributos de un objeto 
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)


    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def movimiento(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def colision(self, obj):
        return choque(self, obj)


class Avion:
    COOLDOWN = 30 #medio segundo 

    #x y son para determinar la posicion, health = 100 se la da un valor defacult 
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None # imagen que usa para cada "ship"
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0 #delay hasta que el usuario puede disparar de nuevo 

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    #chequea por colisiones con obj. Dependiendo si esta en player o enemy 

    def disparo_proyectil(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.movimiento(vel)
            if laser.off_screen(constantes.ALTO):
                self.lasers.remove(laser)
            elif laser.colision(obj):
                obj.health -= 10
                pygame.mixer.Channel(2).play(constantes.SONIDO_EXPLOSION)
                self.lasers.remove(laser)
    #Si el cooldown es mayor que medio seguro, no hace nada. Si es mayor que cero entonces suma 1 
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0: #delay
            laser = Proyectil(self.x, self.y, self.laser_img)
            # pygame.mixer.Channel(0).play(laser_sound)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    #tomo el ancho y el alto para que no se escape de la ventana 
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


#es una clase abstracta, vamos a heredear de esta clase 
class Jugador(Avion):

    def __init__(self, x, y, health=100):
        #super crea una clase que va a heredar todos los methods y propiedades de otra clase 
        super().__init__(x, y, health)
        self.ship_img = constantes.AVION_JUGADOR
        self.laser_img = constantes.PROYECTIL_JUGADOR
        #la mask permite hacer colisiones perfectas. De la surface del avioncito 
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health



    def disparo_proyectil(self, vel, objs, score):
        self.cooldown()
        for laser in self.lasers:
            laser.movimiento(vel)
            if laser.off_screen(constantes.ALTO):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.colision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                          
    def draw(self, window):
        super().draw(window)
        self.salud_jugador(window)

    def salud_jugador(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


class Enemigo(Avion):
    #diccionario, con los tipos de proyectiles y su correspondiente avion. Lo veo innesario 
    TIPOS_ENEMIGO = {
                "debil": (constantes.ENEMIGO_DEBIL, constantes.PROYECTIL_CHICO),
                "dificil": (constantes.ENEMIGO_DIFICIL, constantes.PROYECTIL_MEDIO),
                "infierno": (constantes.ENEMIGO_INFIERNO, constantes.PROYECTIL_GRANDE)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        #asigna disparos. SACAR 
        self.ship_img, self.laser_img = self.TIPOS_ENEMIGO[color]
        #mascara del enemigo 
        self.mask = pygame.mask.from_surface(self.ship_img)

    def movimiento(self, vel):
        self.y += vel

    
    def disparo(self):
        if self.cool_down_counter == 0: # delay para volver a disparar 
            laser = Proyectil(self.x-20, self.y, self.laser_img) #instancia un sprite en esa posicion 
            self.lasers.append(laser)
            self.cool_down_counter = 1

#usa las mascaras para determinar si dos objetos se estan sobreponiendo 
#el offset es la distancia entre las dos mascaras 
#retorna true si hay una colision false si no lo hay 
def choque(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None