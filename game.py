import pygame
import sys
import subprocess

# Initialisation de l'interface de code
subprocess.Popen(["python", "interface.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)

# Initialisation de Pygame
pygame.init()

# Définition des paramètres de la fenêtre
TPS = 20
BLOCK_SIZE = 50
WIDTH, HEIGHT = BLOCK_SIZE*18, BLOCK_SIZE*7

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pyrate - Game")
pygame.display.set_icon(pygame.image.load("img\\favicon.ico"))


#création du fond (ca marche pas)
#background_image = pygame.image.load("images\\images\\fond.jpg").convert()

# Charger les images des textures des blocs
#block_texture = pygame.image.load("Desktop\projet\Projet Pyrate\images\images\bloc.pierre.png")


blocks = ["img\\bloc_pierre.png", "img\\bloc_sable.png", "img\\bouteille.png", "img\\caisse.png", "img\\cle.png", "img\\coffre.png",
         "img\\Palmier.png", "img\\Pierre.png", "img\\pont.png", "img\\Tonneau.png"]

assets = [("img\\fond.png", (WIDTH, HEIGHT)), ("img\\bloc_pierre.png", (BLOCK_SIZE, BLOCK_SIZE)), ("img\\bloc_sable.png", (BLOCK_SIZE, BLOCK_SIZE)), ("img\\bouteille.png", (BLOCK_SIZE/1.5, BLOCK_SIZE)), ("img\\caisse.png", (BLOCK_SIZE, BLOCK_SIZE)), ("img\\cle.png", (BLOCK_SIZE, BLOCK_SIZE/1.5)), ("img\\coffre.png", (BLOCK_SIZE, BLOCK_SIZE)),
          ("img\\Palmier.png", (BLOCK_SIZE, BLOCK_SIZE)), ("img\\Pierre.png", (BLOCK_SIZE, BLOCK_SIZE/2)), ("img\\pont.png", (BLOCK_SIZE, BLOCK_SIZE/2)), ("img\\Tonneau.png", (BLOCK_SIZE, BLOCK_SIZE))]

block_textures = []
asset_textures = []

for block in blocks:
    block_texture = pygame.transform.scale(pygame.image.load(block), (BLOCK_SIZE, BLOCK_SIZE))
    block_textures.append(block_texture)

for asset in assets:
    asset_texture = pygame.transform.scale(pygame.image.load(asset[0]), asset[1])
    asset_textures.append(asset_texture)

# Définir la matrice de la map
map_matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 3, 0, 7, 0, 8, 0, 9, 0, 0, 0, 0, 6],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

# Boucle principale
running = True
clock = pygame.time.Clock()

while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(asset_textures[0], (0, 0))

    # Dessin de la map block par block avec la texture
    for row_index, row in enumerate(map_matrix):
        for col_index, block_type in enumerate(row):
            x = col_index * BLOCK_SIZE
            y = row_index * BLOCK_SIZE

            if block_type != 0:
                screen.blit(asset_textures[block_type], (x, y))

    # Rafraîchissement de l'écran
    pygame.display.flip()

    # Limite de tick par seconde
    clock.tick(TPS)

# Quitter Pygame
pygame.quit()
sys.exit()


