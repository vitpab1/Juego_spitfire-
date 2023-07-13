import pygame
import random
import clases 
import constantes
import ingreso_score


pygame.font.init() 
pygame.mixer.init()

#titulo 
pygame.display.set_caption("Spitfire")

def main():
    ejecucion = True
    FPS = 60

    nivel = 0
    vidas = 1
    score = 0 


    main_font = pygame.font.SysFont("comicsans", 40) #fuente principal y su tamaño 
    pierde_partida_fuente = pygame.font.SysFont("comicsans", 60) 

    # Guarda a los enemigos, define la ola inicial y en cada nivel los incrementa 
    enemigos = []
    enemigos_cantidad_original = 0
    oleada_largo = 10
    enemigo_vel = 1

    jugador_vel = 5
    disparo_vel = 5
    


    jugador = clases.Jugador(350, 700)
    #Usa clock para correr el juego a 60 frames por seg 
    clock = pygame.time.Clock()

    pierde_partida = False
    pierde_partida_cantidad = 0

    def redraw_window():
        #win es una superficie, 0,0 es la esquina sup. izquierda. 
        constantes.WIN.blit(constantes.FONDO_PRIMER_NIVEL, (0,0))
        # draw text
        #lo rendereiza con la variable lives, el 1 es el antialias, rgb  
        vidas_texto = main_font.render(f"Score: {score}", 1, (255,255,255))
        niveles_texto = main_font.render(f"Nivel: {nivel}", 1, (255,255,255))

        #se posiciona 10px arriba, 10 px a la izquierda 
        constantes.WIN.blit(vidas_texto, (10, 820))
        #get_width es un method que se puede usar en surfaces para saber el ancho 
        constantes.WIN.blit(niveles_texto, (constantes.ANCHO - niveles_texto.get_width() - 10, 820))

        #Spawnea enemigos 
        for enemy in enemigos:
            enemy.draw(constantes.WIN)

        jugador.draw(constantes.WIN)

        #60 veces por segundo, refresca la pantalla y actualiza todo 
        pygame.display.update()


    while ejecucion:
        clock.tick(FPS)
        redraw_window()


        #pierde 
        if vidas <= 0 or jugador.health <= 0:
            pierde_partida = True
            pierde_partida_cantidad += 1
            ingreso_score.ingreso_score(score)
        
    
        #cuando no hay mas enemigos en pantalla, se le suma un nivel.
        #Se generan a distitnas alturas por encima de la pantalla visible, y van bajando de manera aleatoria 
        if len(enemigos) == 0:
            nivel += 1
            oleada_largo += 5
            score += 100
            for i in range(oleada_largo):
                enemigo = clases.Enemigo(random.randrange(50, constantes.ANCHO-100), random.randrange(-1500, -100), random.choice(["debil", "dificil", "infierno"]))
                enemigos.append(enemigo)

            
        #chequea si ocurre algun evento 60 veces por segundo |  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        #restringe que no se vaya de la screen para la izquierda usa cero y para la derecha el ancho 
        if keys[pygame.K_a] and jugador.x - jugador_vel > 0: # left
            jugador.x -= jugador_vel
        if keys[pygame.K_d] and jugador.x + jugador_vel + jugador.get_width()  < constantes.ANCHO: # #toma el ancho del jugador para que no se pasa de la ventana 
            jugador.x += jugador_vel
        if keys[pygame.K_w] and jugador.y - jugador_vel > 0: # up
            jugador.y -= jugador_vel
        if keys[pygame.K_s] and jugador.y + jugador_vel + jugador.get_height() + 15 < constantes.ALTO: # down
            jugador.y += jugador_vel
        if keys[pygame.K_SPACE]:
            jugador.shoot()

        #spawnea enemigos. Se hace una copia [:] para que no modifique la lista original 
        for enemigo in enemigos[:]:
            enemigo.movimiento(enemigo_vel)
            enemigo.disparo_proyectil(disparo_vel, jugador)


            if random.randrange(0, 2*60) == 1:
                enemigo.shoot()

            if clases.choque(enemigo, jugador):
                jugador.health -= 100
                enemigos.remove(enemigo) 

                #Si llega al final se elimina el enemigo 
            elif enemigo.y + enemigo.get_height() > constantes.ALTO:
            
                enemigos.remove(enemigo)

        jugador.disparo_proyectil(-disparo_vel, enemigos, score)

        score = (oleada_largo - len(enemigos)) * (nivel + 10)



def menu_principal():
    font = pygame.font.SysFont("comicsans", 50)
    ejecucion = True
    while ejecucion:
        constantes.WIN.blit(constantes.FONDO_PRIMER_NIVEL, (0,0))
        titulo_texto_surface = font.render("Presione click para comenzar", 1, (255,255,255))
        constantes.WIN.blit(titulo_texto_surface, (constantes.ANCHO/2 - titulo_texto_surface.get_width()/2, 350))
        pygame.display.update()
        pygame.mixer.Channel(1).play(constantes.MUSICA_JUEGO)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecucion = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

menu_principal()
