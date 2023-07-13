import pygame
import sys
import re
import scores
import constantes
import mostrar_top_scores

pygame.init()

def ingreso_score(score):
    base_font = pygame.font.SysFont(None, 32)
    pierde_partida_fuente = pygame.font.SysFont("comicsans", 42)
    aclaracion = pygame.font.SysFont("comicsans", 25)

    user_text = ''
    input_rect = pygame.Rect(250, 520, 140, 32)

    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive

    active = False
    max_chars = 20

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(user_text) > 0:
                        scores.insert_score(score, user_text)
                        user_text = ''
                        mostrar_top_scores.mostrar_top_scores()
                else:
                    if re.match(r'^[a-zA-Z]*$', event.unicode) and len(user_text) < max_chars:
                        user_text += event.unicode

        constantes.WIN.fill((143, 188, 143))

        if active:
            color = color_active
        else:
            color = color_passive

        pierde_texto = pierde_partida_fuente.render(f"Perdiste! Tu puntuaje es: {score}", 1, (255, 255, 255))
        escribi_nombre = pierde_partida_fuente.render("Escribi tu nombre", 1, (255, 255, 255))
        condiciones_nombre = aclaracion.render("Solo letras. Max 20 caracteres", 1, (255, 255, 255))

        constantes.WIN.blit(pierde_texto, (40, 350))
        constantes.WIN.blit(escribi_nombre, (40, 400))
        constantes.WIN.blit(condiciones_nombre, (40, 450))

        pygame.draw.rect(constantes.WIN, color, input_rect)

        text_surface = base_font.render(user_text, True, (255, 255, 255))
        constantes.WIN.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        input_rect.w = max(100, text_surface.get_width() + 10)


        pygame.display.flip()