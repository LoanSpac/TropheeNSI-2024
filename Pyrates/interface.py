from os import system
import tkinter as tk
from tkinter.font import Font

## La zone de texte a été créé à l'aide de cette réponse : ##
#  --> https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget
## Cela permet d'avoir une zone de texte avec le numéro des lignes ##

# Cette classe est un canvas tkinter pour les numéros
class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None: return
            y = dline[1]
            linenum = str(i).split(".")[0]

            # Police d'écriture des numéros
            self.create_text(2, y, anchor="nw", text=linenum, font=("Calibri", "20"))
            i = self.textwidget.index("%s+1line" % i)


# Cette classe est un texte d'entré tkinter
class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result


# Création de la zone de texte en tant que frame tkinter
class TextApp(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # On défini un texte tkinter dont on associe la police et la couleur
        self.text = CustomText(self, font=("Segoe UI", "24"), background='#fff')
        font = Font(font=self.text['font'])

        # On configure la longueur de la tabulation
        tab = font.measure('        ')
        self.text.config(tabs=tab)

        # On ajoute une scrollbar pour notre zone de texte
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))

        # On définis le canvas des lignes associant aussi la couleur
        self.linenumbers = TextLineNumbers(self, width=30, background='#fff') # COLOR 2
        self.linenumbers.attach(self.text)

        # On affiche la scollbar, les lignes et le texte
        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        # On configure les touches pour la zone de texte
        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

        # Insert le code par défaut dans le texte
        self.text.insert("end", "from game import *\n\n\n\nlancer()")

        # Créer un menu pour y mettre le bouton "run"
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        menubar.add_checkbutton(label="Run", command=self.save_and_run)

    # Actualise les numéros de ligne
    def _on_change(self, event):
        self.linenumbers.redraw()

    # Sauvegarde et execute le code écrit
    def save_and_run(self):
        with open('niveaux.txt', 'r') as file:
            lines = file.readlines()[8:17]
            limite = str(float(lines[8].replace('\n', ''))+1)

        with open('pyrates_code.py', 'w') as file:
            file.write(self.text.get('1.0', limite))
        system("pyrates_code.py")

# Démarre le programme
if __name__ == '__main__':
    root = tk.Tk()

    # On prend une proportion précise pour l'affichage de la fenêtre
    width, height = root.winfo_screenwidth() / 3.415, root.winfo_screenheight() / 1.28

    # Configuration de la fenêtre
    root.title("Pyrates - Code")
    root.geometry(f"{round(width)}x{round(height)}")
    root.iconbitmap("img/favicon.ico")

    # On affiche la zone de texte
    TextApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
