import tkinter as tk
from tkinter import filedialog, simpledialog
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
        layerFiles = filedialog.askopenfilenames()

        for files in layerFiles:
            pass

    def addLayerSubmenu(self, layer):
        layerMenu = LayerMenu(self, layer)

        self.add_cascade(menu= layerMenu, label = layer)

class GeoPrefsMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_command(label='Not yet implemented', state='disabled')

class LayerMenu(tk.Menu):
    def __init__(self, parent, layer):
        super().__init__(parent)

        self.parent = parent
        self.layer = layer

        #change layer name
        self.add_command(label = "Change Layer Name", command=self.changeName)

        #change layer symbols
        layerSymbolMenu = tk.Menu(self)
        self.add_cascade(menu=layerSymbolMenu, label = 'Change Symbology')

        layerSymbolMenu.add_command(label='Point Symbol', command= self.openPointSymDia)
        layerSymbolMenu.add_command(label='Line Symbol', command= self.openLineSymDia)
        layerSymbolMenu.add_command(label='Polygon Symbol', command= self.openPolygonSymDia)

        #export layer data
        self.add_command(label='Save Source Data...', command= self.layer.saveData)
        self.add_command(label='Save New Data File...', command= self.saveToFile)

        #change display field
        self.add_command(label='Change Display Field', command=self.changeDisplay)

        #change selectable
        self.selectable = tk.BooleanVar(self,True)
        self.add_checkbutton(label='Selectable', variable= self.selectable, onvalue= True, offvalue= False)

        self.selectable.trace_add("write", self.changeSelectable)

        #save layer file
        self.add_command(label='Create Layer File', command=layer.saveLayerAsFile)

        #open layer table
        self.add_command(label= 'Open Table', command=self.openTable)

        #remove layer
        self.add_command(label='Remove Layer', command=self.removeLayer)

    def openPointSymDia(self):
        PointSymbolDialog(self.layer)

    def openLineSymDia(self):
        LineSymbolDialog(self.layer)

    def openPolygonSymDia(self):
        PolygonSymbolDialog(self.layer)

    def changeSelectable(self, *_):
        self.layer.setSelectable(self.selectable.get())

    def changeDisplay(self):
        field = simpledialog.askstring('Display Field', 'Enter field to name entities in attribute window:')

        if field:
            try:
                self.layer.gdf[field]
            except KeyError:
                print("Invalid Disply Field, no such column with name.")
            else:
                self.layer.displayField = field

    def changeName(self):
        name = simpledialog.askstring('Set Layer Name', 'Enter new name for layer:')

        if name:
            self.parent.entryconfig(self.layer.name, label = name)

            self.layer.changeName(name)

    def saveToFile(self):
        file = filedialog.asksaveasfilename(confirmoverwrite=True, filetypes=[('Shapefile', '*.shp')] )

        if file:
            self.layer.saveData(file)
            
    def openTable(self):
        AttributeTable(self.layer)

    def removeLayer(self):
        self.layer.removeSelf()

        self.destroy()
