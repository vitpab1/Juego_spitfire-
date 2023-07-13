import pygame
import sqlite3
import constantes


def mostrar_top_scores():
    pygame.init()



    pierde_partida_fuente = pygame.font.SysFont("comicsans", 42) 

    window = constantes.WIN
   
    connection = sqlite3.connect('scores.db')
    cursor = connection.cursor()


    cursor.execute("SELECT nombre, score FROM jugadores ORDER BY score DESC LIMIT 10")
    top_scores = cursor.fetchall()


    cursor.close()
    connection.close()


    font = pygame.font.Font(None, 30)
    y = 150
    constantes.WIN.fill((143, 188, 143))

    muestra_puntajes = pierde_partida_fuente.render(f"Mejores puntajes", 1, (255, 255, 255))
    constantes.WIN.blit(muestra_puntajes, (180, 20))    

    for i, (nombre, score) in enumerate(top_scores, 1):

        score = int(score) if score.is_integer() else score
        score_text = f"{i}. {nombre}: {score}"
        text_surface = font.render(score_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(window.get_width() // 2, y))
        window.blit(text_surface, text_rect)
        y += 30


    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()