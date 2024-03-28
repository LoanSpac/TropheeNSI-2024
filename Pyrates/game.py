import pygame
import sys
from main import draw_text

# Définition de la liste des instructions à utiliser
instructions = []

class Pyrates:
    def __init__(self):

        # Initialisation de Pygame
        pygame.init()

        # Définition des paramètres de la fenêtre
        self.TPS = 20
        self.BLOCK_SIZE = 50
        self.WIDTH, self.HEIGHT = self.BLOCK_SIZE * 18, self.BLOCK_SIZE * 7

        # Création de la fenêtre
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pyrates - Game")
        pygame.display.set_icon(pygame.image.load("img\\favicon.ico"))

        # Chargement des assets
        self.assets = [("img\\fond.png", (self.WIDTH, self.HEIGHT)), ("img\\bloc_pierre.png", (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                  ("img\\bloc_sable.png", (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                  ("img\\bouteille.png", (self.BLOCK_SIZE / 1.5, self.BLOCK_SIZE)), ("img\\caisse.png", (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                  ("img\\cle.png", (self.BLOCK_SIZE, self.BLOCK_SIZE / 1.5)),
                  ("img\\coffre.png", (self.BLOCK_SIZE, self.BLOCK_SIZE)), ("img\\Palmier.png", (self.BLOCK_SIZE, self.BLOCK_SIZE)),
                  ("img\\Pierre.png", (self.BLOCK_SIZE, self.BLOCK_SIZE / 2)), ("img\\pont.png", (self.BLOCK_SIZE, self.BLOCK_SIZE / 2)),
                  ("img\\Tonneau.png", (self.BLOCK_SIZE, self.BLOCK_SIZE)), ("img\\Jack.png", (self.BLOCK_SIZE, self.BLOCK_SIZE))]

        self.asset_textures = []

        for asset in self.assets:
            asset_texture = pygame.transform.scale(pygame.image.load(asset[0]), asset[1])
            self.asset_textures.append(asset_texture)

        # Définition de la grille du niveau
        with open('niveaux.txt', 'r') as file:
            lines = file.readlines()[8:15]
            self.map_matrice = []
            for line in lines:
                ligne = list(map(int, (line.replace('\n', '')).split(", ")))
                for block in ligne:
                    if block == 11:
                        ligne[ligne.index(block)] = (11, 0)
                self.map_matrice.append(ligne)

        # Définition des paramètres en jeu
        self.running = True
        self.clock = pygame.time.Clock()
        self.solides = [1, 2, 3, 4, 8, 9]
        self.anim = 0
        self.flip = False
        self.var_avancer = False
        self.var_sauter = False
        self.var_key = False

        # Lancement de la boucle principal du jeu
        while self.running:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Affichage du fond
            self.screen.blit(self.asset_textures[0], (0, 0))

            # Dessin de la map block par block avec la texture
            for row_index, row in enumerate(self.map_matrice):
                for col_index, block_type in enumerate(row):
                    x = col_index * self.BLOCK_SIZE
                    y = row_index * self.BLOCK_SIZE

                    # Affichage des blocks du jeu
                    if block_type != 0 and type(block_type) == int:
                        self.screen.blit(self.asset_textures[block_type], (x, y))

                    # Traitement du personnage
                    elif type(block_type) == tuple:
                        if self.anim < 1:
                            # Execution d'une instruction
                            if instructions != []:
                                if instructions[0] == "droite":
                                    self.droite()
                                    self.flip = True
                                elif instructions[0] == "gauche":
                                    self.gauche()
                                    self.flip = False
                                elif instructions[0] == "avancer":
                                    self.anim = 1
                                    self.var_avancer = True
                                elif instructions[0] == "sauter":
                                    self.anim = 1
                                    self.var_sauter = True
                                elif instructions[0] == "ouvrir":
                                    self.ouvrir((row_index, col_index))
                                instructions.remove(instructions[0])

                            # Affichage du personnage (statique)
                            self.screen.blit(self.asset_textures[11], (x, y))

                            # Récupère la clé pour le personnage
                            if block_type[1] == 5:
                                self.var_key = True
                                self.map_matrice[row_index][col_index] = (11, 0)
                        else:
                            # Avancement du personnage
                            if self.var_avancer:
                                if (self.flip and self.map_matrice[row_index][col_index + 1] in self.solides) or (not self.flip and self.map_matrice[row_index][col_index - 1] in self.solides):
                                    self.anim = 0
                                    instructions.clear()
                                    print("Vous êtes bloqué.")
                                    break
                                self.anim = self.avancer(x, y, (row_index, col_index))
                                if self.anim == 0 and ((self.flip and self.map_matrice[row_index + 1][col_index + 1] not in self.solides) or (not self.flip and self.map_matrice[row_index + 1][col_index - 1] not in self.solides)):
                                    self.anim = 1

                            # Saut du personnage
                            elif self.var_sauter:
                                self.anim = self.sauter(x, y, (row_index, col_index))
                                if self.anim == 0:
                                    if (self.flip and self.map_matrice[row_index][col_index + 1] in self.solides) or (not self.flip and self.map_matrice[row_index][col_index - 1] in self.solides):
                                        self.anim = 1
                                        self.var_avancer = True
                                    else:
                                        self.anim = 1

                            # Chute du personnage
                            else:
                                self.anim = self.tomber(x, y, (row_index, col_index))
                                if self.anim == 0 and self.map_matrice[row_index + 2][col_index] not in self.solides:
                                    self.anim = 1

            # Rafraîchissement de l'écran
            pygame.display.flip()

            # Limite de tick par seconde
            self.clock.tick(self.TPS)

        self.victoire()

        # Quitter Pygame
        pygame.quit()
        sys.exit()

    def victoire(self, running=True):
        # Lancement de la boucle principal du jeu
        while running:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Affichage du fond
            self.screen.blit(self.asset_textures[0], (0, 0))

            draw_text("Vous avez gagné !", pygame.font.Font(None, 36), (0, 0, 0), self.screen, 300, 100)

            # Rafraîchissement de l'écran
            pygame.display.flip()

            # Limite de tick par seconde
            self.clock.tick(self.TPS)

    # Méthode pour tourner le personnage à droite
    def droite(self):
        if not self.flip:
            self.asset_textures[11] = pygame.transform.flip(self.asset_textures[11], True, False)

    # Méthode pour tourner le personnage à gauche
    def gauche(self):
        if self.flip:
            self.asset_textures[11] = pygame.transform.flip(self.asset_textures[11], True, False)

    # Méthode pour avancer le personnage
    def avancer(self, x, y, index):
        if self.flip:
            self.screen.blit(self.asset_textures[11], (x + (self.BLOCK_SIZE / 10) * self.anim + 1, y))
        elif not self.flip:
            self.screen.blit(self.asset_textures[11], (x - (self.BLOCK_SIZE / 10) * self.anim + 1, y))
        self.anim += 1
        if self.anim == 11:
            self.map_matrice[index[0]][index[1]] = self.map_matrice[index[0]][index[1]][1]
            if self.flip:
                self.map_matrice[index[0]][index[1] + 1] = (11, self.map_matrice[index[0]][index[1] + 1])
            elif not self.flip:
                self.map_matrice[index[0]][index[1] - 1] = (11, self.map_matrice[index[0]][index[1] - 1])
            self.var_avancer = False
            return 0
        return self.anim

    # Méthode pour faire sauter le personnage
    def sauter(self, x, y, index):
        self.screen.blit(self.asset_textures[11], (x, y - (self.BLOCK_SIZE / 10) * self.anim + 1))
        self.anim += 1
        if self.anim == 11:
            self.map_matrice[index[0]][index[1]] = self.map_matrice[index[0]][index[1]][1]
            self.map_matrice[index[0] - 1][index[1]] = (11, self.map_matrice[index[0] - 1][index[1]])
            self.var_sauter = False
            return 0
        return self.anim

    # Méthode pour faire tomber le personnage
    def tomber(self, x, y, index):
        self.screen.blit(self.asset_textures[11], (x, y + (self.BLOCK_SIZE / 10) * self.anim + 1))
        self.anim += 1
        if self.anim == 11:
            self.map_matrice[index[0]][index[1]] = self.map_matrice[index[0]][index[1]][1]
            self.map_matrice[index[0] + 1][index[1]] = (11, self.map_matrice[index[0] + 1][index[1]])
            return 0
        return self.anim

    def ouvrir(self, index):
        if self.map_matrice[index[0]][index[1]] == (11, 6) and self.var_key: # And verify Key
            self.running = False
        else:
            print("Tu ne peux pas ouvrir.")

# Définition des instructions possible
def droite():
    instructions.append("droite")

def gauche():
    instructions.append("gauche")

def avancer():
    instructions.append("avancer")

def sauter():
    instructions.append("sauter")

def ouvrir():
    instructions.append("ouvrir")

def pygame_wrapper(coro):
    yield from coro

# Fonction pour lancer le jeu
def lancer():
    game = Pyrates()
    wrap = pygame_wrapper(game)
    wrap.send(None) # prime the coroutine
    return game
