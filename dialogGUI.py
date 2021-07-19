import mplElements
import tkinter as tk
from tkinter import ttk
from layerClasses import Layer
from tkinter import filedialog

class AttributeDialog(tk.Toplevel):
    #attribute defining currently open window, so that we can assure that there is only one
    existingWindow = None

    def openOrAdd(entity):
        '''Determine if entity should be added to an existing window or create a new window'''
        #Add a new entity to the existing window
        if AttributeDialog.existingWindow:
            AttributeDialog.existingWindow.addEntity(entity)

        #Create a window with the entity
        else:
            AttributeDialog(entity)

    def __init__(self,entity):
        super().__init__()

        #initial window properties
        self.title('Edit Attributes')
        self.minsize(250,350)
        self.attributes('-topmost', 'true')
        self.entities = [entity]

        #handling for when window is closed
        self.protocol("WM_DELETE_WINDOW", self.closeWindow)

        #Create attribute frame for holding attributes/values
        self.attributeFrame = ttk.Frame(self, borderwidth=2, relief= "sunken")
        self.attributeFrame.pack(side="bottom", fill="both", expand= True, pady= 20, padx= 20)

        #Create a canvas/scroll area to handle the sizing of 
        #height and width set lower than window minimum + other components so that it will expand to fill available space
        self.attributeCanvas = tk.Canvas(self.attributeFrame, height=100, width= 100)
        self.attributeScrollArea = ttk.Frame(self.attributeCanvas, padding= 10)

        #Create and link scrollbar to canvas, add elements to the attribute frame
        self.attributeScrollbar = ttk.Scrollbar(self.attributeFrame, orient= tk.VERTICAL, command=self.attributeCanvas.yview )
        self.attributeCanvas.configure(yscrollcommand=self.attributeScrollbar.set)
        self.canvasFrame = self.attributeCanvas.create_window((0,0), window=self.attributeScrollArea, anchor='nw')
        self.attributeScrollbar.pack(side="right",fill="y")
        self.attributeCanvas.pack(side="left", fill="both", expand=True, padx= 10, pady = 10)

        #handle resizing of scroll area to match canvas
        self.attributeCanvas.bind("<Configure>", self._resizeAttributeCanvas)

        #Make attribute value column expandable
        self.attributeScrollArea.columnconfigure(1, weight=1)

        #Add dropdown for selecting an active entity
        self.selectedEntity = entity
        self.selectedEntityVar = tk.StringVar()
        self.entitySelector = ttk.OptionMenu(self, self.selectedEntityVar, entity, *self.entities, command=self.changeEntity)
        self.entitySelector.pack(side="top", fill = 'both', pady = 10, padx = 30)

        #Add buttons for controlling edit functions
        self.applyEditsBtn = ttk.Button(self, text="Apply", command=self.applyEdits, state="disabled")
        self.cancelEditsBtn = ttk.Button(self, text="Discard", command=self.cancelEdits, state="disabled")
        self.removeEntityBtn = ttk.Button(self, text= "X", command=self.removeEntity, width= 2, state = "disabled")

        self.applyEditsBtn.pack(side='right')
        self.cancelEditsBtn.pack(side='right')
        self.removeEntityBtn.pack(side='left')

        #Add label for number of entities in menu
        self.entityCount = tk.IntVar(value= len(self.entities))
        self.entityCountLabel = ttk.Label(self,textvariable=self.entityCount)
        self.entityCountLabel.pack(side='left')

        AttributeDialog.existingWindow = self
        self.fillAttibutes(entity)

        self.editedAttributes = {}
        self.editing = 'off' #indicates whether any 

    def closeWindow(self):
        AttributeDialog.existingWindow = None
        self.destroy()

    def fillAttibutes(self,entity):
        #clear out everything in the scroll area
        children = self.attributeScrollArea.winfo_children()
        for child in children:
            child.destroy()
            
        self.attributes = {} #collector for labels/values to ensure they are accessible later
        for i, col in enumerate(entity.gdfRow.index):
            attName = ttk.Label(self.attributeScrollArea, text= col)
            attValue = tk.StringVar(value= entity.gdfRow[col])
            textEntry = ttk.Entry(self.attributeScrollArea, textvariable=attValue)

            self.attributes[i] = [attName,textEntry,attValue]
            
            #attach variable changes to callback function, using lambda to also send entry box and label
            attValue.trace_add('write', lambda var, ind, mode, entry = textEntry, label = attName, value = attValue: self.attributeChanged(entry , label, value))
            
            attName.grid(row = i, column= 0, pady= 7)
            textEntry.grid(row= i, column= 1, pady= 7,sticky=(tk.E,tk.W) )

    def changeEntity(self,entity):
        self.selectedEntity = entity
        self.fillAttibutes(entity)

    def _resizeAttributeCanvas(self,event):
        canvasWidth = event.width
        self.attributeCanvas.itemconfig(self.canvasFrame, width = canvasWidth)
        self.attributeCanvas.configure(scrollregion= self.attributeCanvas.bbox("all"))

    def addEntity(self,entity):
        if entity not in self.entities:
            self.entities.append(entity)
            self.entitySelector.set_menu(self.entitySelector.grab_current(), *self.entities)

            if len(self.entities) > 1 and self.editing == 'off':
                self.removeEntityBtn.configure(state="enabled")
                self.entityCount.set(len(self.entities))

    def applyEdits(self):
        for label in self.editedAttributes:
            entryBox = self.editedAttributes[label][0]

            self.selectedEntity.gdfRow[label.cget("text")] = entryBox.get()

        self.editingSwitch('off')

    def cancelEdits(self):
        for label in self.editedAttributes:
            value = self.editedAttributes[label][1]

            value.set( self.selectedEntity.gdfRow[label.cget("text")] )

        self.editingSwitch('off')

    def removeEntity(self):
        if len(self.entities) > 1:
            self.entities.remove(self.selectedEntity)

            self.selectedEntity = self.entities[-1]
            self.entitySelector.set_menu(self.entities[-1], *self.entities)
            self.fillAttibutes(self.selectedEntity)

            if len(self.entities) == 1:
                self.removeEntityBtn.configure(state='disabled')
        
        self.entityCount.set(len(self.entities))

    def attributeChanged(self, entry, label, value):
        self.editingSwitch('on')

        self.editedAttributes[label] = [entry,value]

        label.configure(font="bold")

    def editingSwitch(self, turn):
        self.editing = turn

        self.applyEditsBtn.configure(state="enabled" if turn == 'on' else 'disabled')
        self.cancelEditsBtn.configure(state="enabled" if turn == 'on' else 'disabled')
        self.removeEntityBtn.configure(state="disabled" if turn == 'on' or len(self.entities) < 2 else 'enabled')
        self.entitySelector.configure(state='disabled' if turn == 'on' else 'enabled')

        if turn == 'off':
            for label in self.editedAttributes:
                label.configure(font="")

            self.editedAttributes = {}
        
class NewLayerDialog(tk.Toplevel):
    def __init__(self, layerMenu):
        super().__init__()

        self.title("Add New Layer")
        self.attributes('-topmost', 'true')

        self.layerMenu = layerMenu

        self.openSourceBtn = ttk.Button(self, command=self.openSource, text="Choose Source")
        self.openSourceBtn.grid(row=0, column=1,padx= 10, pady= 10)

        self.sourceText = tk.StringVar()
        self.sourceEntry = ttk.Entry(self,textvariable=self.sourceText)
        self.sourceEntry.grid(row=0,column=0, padx= 10, pady= 10, sticky=tk.EW)

        self.columnconfigure(0, weight = 1)

        self.createBtn = ttk.Button(self, text= "Create Layer", command=self.createLayer)
        self.createBtn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def openSource(self):
        selectedFile = filedialog.askopenfilename()

        self.sourceText.set(selectedFile)

    def createLayer(self):
        axes = mplElements.GEFigure.figures[-1].subplot

        axesHasData = True if axes.has_data() else False

        newLayer = Layer( self.sourceText.get(), axes)

        if not axesHasData:
            axes.relim()
            axes.autoscale_view()

        mplElements.GEFigure.figures[-1].canvas.draw()

        self.layerMenu.addLayerSubmenu(newLayer)

        self.destroy()

class SymbolDialog(tk.Toplevel):
    def __init__(self, layer):
        super().__init__()
        
        self.title("Symbology Selector")
        self.attributes('-topmost', 'true')
        self.layer = layer

class PointSymbolDialog(SymbolDialog):
    def __init__(self, layer):
        super().__init__(layer)

        self.title(f"Point {self.title}")

class LineSymbolDialog(SymbolDialog):
    def __init__(self, layer):
        super().__init__(layer)

        self.title(f"Line {self.title}")

class PolygonSymbolDialog(SymbolDialog):
    def __init__(self, layer):
        super().__init__(layer)

        self.title(f"Polygon {self.title}")

class AttributeTable(tk.Toplevel):
    def __init__(self, layer):
        super().__init__()

        self.title(layer.name + " Layer Table")

        unavailable = ttk.Label(self, text='Layer tables have not yet been implemented...')
        unavailable.pack(pady=50,padx=50)



