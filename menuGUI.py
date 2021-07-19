import tkinter as tk
from tkinter import filedialog
from dialogGUI import NewLayerDialog

class GeoMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_cascade(menu=GeoFileMenu(self), label='File')
        self.add_cascade(menu=GeoLayerMenu(self), label='Layers')
        self.add_cascade(menu=GeoPrefsMenu(self), label='Preferences')

class GeoFileMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_command(label='New', command=self.newFile)
        self.add_command(label='Open...', command=self.openFile)
        self.add_command(label='Save', command=self.saveFile)
        self.add_command(label='Save As...', command=self.saveFileAs)

    def newFile(self):
        pass

    def openFile(self):
        pass

    def saveFile(self):
        pass

    def saveFileAs(self):
        pass

class GeoLayerMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_command(label='Add New Layer...', command=self.newLayer)
        self.add_command(label='Open Layer File...', command=self.openLayerFile)
        self.add_separator()

    def newLayer(self):
        NewLayerDialog()

    def openLayerFile(self):
        layerFiles = filedialog.askopenfiles()

        for files in layerFiles:
            pass
        
class GeoPrefsMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_command(label='Not yet implemented', state='disabled')