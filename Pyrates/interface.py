from os import system
import tkinter as tk
from tkinter.font import Font

## La zone de texte a été créé à l'aide de cette réponse : ##
# https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget

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
            self.create_text(2, y, anchor="nw", text=linenum, font=("Calibri", "20"))
            i = self.textwidget.index("%s+1line" % i)

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

class TextApp(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self, font=("Segoe UI", "24"), background='#fff') # COLOR 1
        font = Font(font=self.text['font'])
        tab = font.measure('        ')
        self.text.config(tabs=tab)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.linenumbers = TextLineNumbers(self, width=30, background='#fff') # COLOR 2
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

        self.text.insert("end", "from game import *\n\n\n\nlancer()")
        #self.text.insert("end", "four\n",("bigfont",))
        #self.text.insert("end", "five\n")

        # create a menubar
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        menubar.add_checkbutton(label="Run", command=self.save_and_run)

    def _on_change(self, event):
        self.linenumbers.redraw()

    def save_and_run(self):
        with open('pyrates_code.py', 'w') as file:
            file.write(self.text.get('1.0', 'end'))
        # Add lines filter config
        system("pyrates_code.py")

if __name__ == '__main__':
    root = tk.Tk()
    width, height = root.winfo_screenwidth() / 3.415, root.winfo_screenheight() / 1.28

    # configure window
    root.title("Pyrates - Code")
    root.geometry(f"{round(width)}x{round(height)}")
    root.iconbitmap("img/favicon.ico")

    TextApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
