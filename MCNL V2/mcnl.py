import customtkinter
import shutil
from zipfile import ZipFile
import os
from PIL import Image

# Cette classe permet de charger nos boutons dans une frame où l'on peut sroll
class ScrollableNavigationFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.radiobutton_variable = customtkinter.StringVar()
        self.button_list = []

    # Permet d'ajouter un bouton
    def add_item(self, item, image=None, command=None):
        button = customtkinter.CTkButton(self, corner_radius=0, height=40,
                                                      border_spacing=10, text=item,
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=image, anchor="w",
                                                      command=command)

        button.grid(row=len(self.button_list)+1, column=0, sticky="ew")

        self.button_list.append(button)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        ###### DISPLAY GUI ######

        self.title("MCNL V2")
        self.geometry("700x450")

        # On défini la grille 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ###### LOAD IMAGES ######

        # On charge certaines images avec un mod lumineux et sombre
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # On charge toutes les images de matières
        self.matieres_image = [customtkinter.CTkImage(Image.open(os.path.join(image_path, "ArtPlastique.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "BioTechnologie.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "EcoGestion.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "EPS.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "Francais-Litterature.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "Graphisme.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "HistGeo.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "Internet.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "Langues.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "Mathematiques.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "Modelisation3D.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "Musique.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "Philosophie.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "Physique-Chimie.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "SES.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "SII-STI2D.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "SNT-NSI.png"))),
                               customtkinter.CTkImage(Image.open(os.path.join(image_path, "SVT.png")))]

        ##### ACCEUIL FRAME #####

        # On créé l'interface "home" qui va nous afficher une image de test
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        ##### LOAD BUTTONS ######

        # On créé un label scrollable où ajouter les boutons
        self.scrollable_navigation_frame = ScrollableNavigationFrame(master=self, corner_radius=0)
        self.scrollable_navigation_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.scrollable_navigation_frame.grid_rowconfigure(4, weight=1)

        # On définis ici nos items, c'est à dire les matières avec leurs nom de répertoire
        self.items = [("Art Plastique", "art"), ("Bio Technologie", "bio_tech"), ("Eco Gestion", "eco"),
       ("E.P.S.", "eps"), ("Français Littérature", "fr_lit"), ("Graphisme", "graph"), ("Histoire - Geo", "hist_geo"),
       ("Internet", "inter"), ("Langues", "lang"), ("Mathématiques", "math"), ("Modélisation 3D", "model"),
       ("Musique", "musi"), ("Philosophie", "philo"), ("Physique - Chimie", "phys_chim"), ("S.E.S.", "ses"),
       ("SII - STI2D", "sii_sti"), ("SNT - NSI", "snt_nsi"), ("S.V.T.", "svt")]

        self.buttons = []

        # On ajoute chaque boutons au label scrollable
        for i, x in enumerate(self.items):
            button = self.scrollable_navigation_frame.add_item(self.items[i][0], image=self.matieres_image[i], command=lambda i=i,x=x: self.download_and_extract(self.items[i][1]))
            self.buttons.append(button)

        # On défini un autre label avec le titre et l'icone
        self.navigation_frame_label = customtkinter.CTkLabel(self.scrollable_navigation_frame, text="  MCNL V2", image=self.home_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # On sélectionne par défaut la frame
        self.set_frame("home")

    """
    # Fonction en cours d'avancement pour ajouter automatiquement les autres frames
    def button_event(self, index):
        print("test")
        for i in range(len(self.buttons)):
            print(self.buttons)
            button = self.buttons[i]
            button.configure(fg_color=("gray75", "gray25") if self.items[index] == self.items[i] else "transparent")

            if self.items[index] == self.items[i]:
                self.frames[index].grid(row=0, column=1, sticky="nsew")
    """

    # Cette méthode permet de changer d'apparence
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Cette méthode permet de choisir une frame
    def set_frame(self, name):
        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")

    # Cette méthode permet de télécharger et extraire un fichier choisi
    def download_and_extract(self, matiere):
        client_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Client") + '//'
        drive_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Drive MCNL") + '//'
        file = matiere + ".zip"
        source = drive_path + file
        shutil.copy(source, client_path)

        with ZipFile(client_path + file, "r") as zip:
            zip.printdir()
            zip.extractall(client_path)

        os.remove(client_path + file)


if __name__ == "__main__":
    app = App()
    app.mainloop()