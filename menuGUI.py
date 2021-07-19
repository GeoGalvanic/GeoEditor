import tkinter as tk
from tkinter import filedialog
from dialogGUI import NewLayerDialog, PointSymbolDialog, LineSymbolDialog, PolygonSymbolDialog, AttributeTable

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
        NewLayerDialog(self)

    def openLayerFile(self):
        layerFiles = filedialog.askopenfiles()

        for files in layerFiles:
            pass

    def addLayerSubmenu(self, layer):
        layerMenu = LayerMenu(self, layer)

        self.add_cascade(menu= layerMenu, label = str(layer))

class GeoPrefsMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_command(label='Not yet implemented', state='disabled')

class LayerMenu(tk.Menu):
    def __init__(self, parent, layer):
        super().__init__(parent)

        self.layer = layer

        #change layer name
        self.add_command(label = "Change Layer Name", command=self.layer.changeName)

        #change layer symbols
        layerSymbolMenu = tk.Menu(self)
        self.add_cascade(menu=layerSymbolMenu, label = 'Change Symbology')

        layerSymbolMenu.add_command(label='Point Symbol', command= self.openPointSymDia)
        layerSymbolMenu.add_command(label='Line Symbol', command= self.openLineSymDia)
        layerSymbolMenu.add_command(label='Polygon Symbol', command= self.openPolygonSymDia)

        #export layer data
        self.add_command(label='Save Edits...', command= self.layer.saveSource)
        self.add_command(label='Save New Data File...', command= self.layer.saveToFile)

        #discard layer edits
        self.add_command(label= 'Discard Edits' , command= layer.discardEdits)

        #change display field
        self.add_command(label='Change Display Field', command=self.layer.changeDisplay)

        #change selectable
        self.selectable = tk.BooleanVar(self,True)
        self.add_checkbutton(label='Selectable', variable= self.selectable, onvalue= True, offvalue= False)

        self.selectable.trace_add("write", self.changeSelectable)

        #save layer file
        self.add_command(label='Create Layer File', command=layer.saveLayerAsFile)

        #open layer table
        self.add_command(label= 'Open Table', command=self.openTable)

    def openPointSymDia(self):
        PointSymbolDialog(self.layer)

    def openLineSymDia(self):
        LineSymbolDialog(self.layer)

    def openPolygonSymDia(self):
        PolygonSymbolDialog(self.layer)

    def changeSelectable(self, *_):
        self.layer.setSelectable(self.selectable.get())

    def openTable(self):
        AttributeTable(self.layer)

