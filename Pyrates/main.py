from os import system
import pygame
import sys

# Permet d'écrire un texte
def draw_text(text, font, color, surface, x, y):
    # On défini la police
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)

    # Affichage du texte
    surface.blit(text_obj, text_rect)

# Permet d'afficher le menu
def menu():
    while True:
        # Affichage du fond
        screen.blit(pygame.transform.scale(pygame.image.load("img\\fond.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        # Dessin du titre
        draw_text(" Pyrates V2", font, BLACK, screen, 325, 100)

        # Dessin des boutons
        pygame.draw.rect(screen, RED, (300, 200, 200, 50))
        draw_text("   Lancer", font, BLACK, screen, 340, 210)

        pygame.draw.rect(screen, RED, (280, 300, 250, 50))
        draw_text(" Editeur de niveau", font, BLACK, screen, 285, 310)

        pygame.display.update()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 500 and 200 <= mouse_pos[1] <= 250:
                    # Redirection vers le niveau 1
                    pygame.quit()

                    # On ouvre le programme "interface" avec python.
                    system("interface.py")
                    sys.exit()
                elif 300 <= mouse_pos[0] <= 500 and 300 <= mouse_pos[1] <= 350:
                    # Redirection vers l'éditeur de jeu
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__':
    # Initialisation de Pygame
    pygame.init()
    pygame.display.set_caption("Pyrates - Menu")
    pygame.display.set_icon(pygame.image.load("img\\favicon.ico"))

    # Définition des couleurs
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Définition des dimensions de la fenêtre
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # Création de la fenêtre
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Police du texte
    font = pygame.font.Font(None, 36)

    menu()