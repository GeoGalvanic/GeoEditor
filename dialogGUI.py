import mplElements
import tkinter as tk
from tkinter import ttk
from layerClasses import Layer
from tkinter import filedialog, colorchooser, messagebox
from traceback import format_exception
from sys import exc_info

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

        try:
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
            self.editing = 'off' #indicates whether any editing is being done

        except:
            ErrorDialog(f'Initializing an Attribute Editor')

    def closeWindow(self):
        AttributeDialog.existingWindow = None
        self.destroy()

    def fillAttibutes(self,entity):
        try:
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

        except:
            ErrorDialog("(Re)filling the attributes in the attribute editor")

    def changeEntity(self,entity):
        self.selectedEntity = entity
        self.fillAttibutes(entity)

    def _resizeAttributeCanvas(self,event):
        try:
            canvasWidth = event.width
            self.attributeCanvas.itemconfig(self.canvasFrame, width = canvasWidth)
            self.attributeCanvas.configure(scrollregion= self.attributeCanvas.bbox("all"))
        except:
            ErrorDialog("Resizing the canvas in attribute editor")

    def addEntity(self,entity):
        try:
            if entity not in self.entities:
                self.entities.append(entity)
                self.entitySelector.set_menu(self.entitySelector.grab_current(), *self.entities)

                if len(self.entities) > 1 and self.editing == 'off':
                    self.removeEntityBtn.configure(state="enabled")
                    self.entityCount.set(len(self.entities))
        except:
            ErrorDialog(f'Adding {entity} to the attibute editor')

    def applyEdits(self):
        try:
            for label in self.editedAttributes:
                entryBox = self.editedAttributes[label][0]

                self.selectedEntity.layer.gdf.loc[
                    (self.selectedEntity.gdfIndex,label.cget("text"))
                    ] = entryBox.get()

            self.editingSwitch('off')
        except:
            ErrorDialog(f'Applying the edits of {self.selectedEntity}')

    def cancelEdits(self):
        try:
            for label in self.editedAttributes:
                value = self.editedAttributes[label][1]

                value.set( self.selectedEntity.gdfRow[label.cget("text")] )

            self.editingSwitch('off')
        except:
            ErrorDialog(f'Canceling edits on {self.selectedEntity}')

    def removeEntity(self, entity = None):
        if len(self.entities) > 1:

            try:
                entity = entity if entity else self.selectedEntity

                self.entities.remove(entity)

                if entity == self.selectedEntity:
                    self.selectedEntity = self.entities[-1]
                    self.entitySelector.set_menu(self.entities[-1], *self.entities)
                    self.fillAttibutes(self.selectedEntity)

                if len(self.entities) == 1:
                    self.removeEntityBtn.configure(state='disabled')

            except:
                ErrorDialog(f'Removing {entity} from the attribute editor')
        
        self.entityCount.set(len(self.entities))

    def attributeChanged(self, entry, label, value):
        self.editingSwitch('on')

        self.editedAttributes[label] = [entry,value]

        label.configure(font="bold")

    def editingSwitch(self, turn):
        self.editing = turn

        try:
            self.applyEditsBtn.configure(state="enabled" if turn == 'on' else 'disabled')
            self.cancelEditsBtn.configure(state="enabled" if turn == 'on' else 'disabled')
            self.removeEntityBtn.configure(state="disabled" if turn == 'on' or len(self.entities) < 2 else 'enabled')
            self.entitySelector.configure(state='disabled' if turn == 'on' else 'enabled')

            if turn == 'off':
                for label in self.editedAttributes:
                    label.configure(font="")

                self.editedAttributes = {}
        except:
            ErrorDialog(f'Turning editing {turn} in attribute editor')
        
class NewLayerDialog(tk.Toplevel):
    def __init__(self, layerMenu):
        super().__init__()
        try:
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
        except:
            ErrorDialog("Creating new layer dialog")

    def openSource(self):
        selectedFile = filedialog.askopenfilename(filetypes=[("Shapefile", "*.shp")] )

        self.sourceText.set(selectedFile)

    def createLayer(self):
        try:
            axes = mplElements.GEFigure.figures[-1].subplot

            axesHasData = True if axes.has_data() else False

            newLayer = Layer( self.sourceText.get(), axes)

            if not axesHasData:
                axes.relim()
                axes.autoscale_view()

            mplElements.GEFigure.figures[-1].canvas.draw()

            self.layerMenu.addLayerSubmenu(newLayer)

            self.destroy()
        except:
            ErrorDialog(f'Creating new layer from {self.sourceText}')

class SymbolDialog(tk.Toplevel):
    def __init__(self, layer):
        super().__init__()
        
        self.title("Symbology Selector")
        self.attributes('-topmost', 'true')
        self.layer = layer

        #Make second column exandable
        self.columnconfigure(1, weight = 1)

    def promptColor(self, color):
        return colorchooser.askcolor(color)

class PointSymbolDialog(SymbolDialog):
    def __init__(self, layer):
        super().__init__(layer)

        self.title("Point Symbology Selector")

        self.currentVals = self.layer.pointSymbology

        try:
            #Dictionary to lookup common shape names compared to their MPL marker style string
            self.valueLookup = {
                'Circle' :   'o',
                'Triangle' : '^',
                'Square' :   's',
                'Star' :     '*',
                'Plus' :     'P',
                'Cross' :    'X',
                'Diamond' :  'd'
            }

            #Input widgets for defining the shape/marker of point symbols
            self.markerLabel = ttk.Label(self, text='Shape: ')
            self.markerLabel.grid(column=0, row = 0, padx=10,pady=10)

            self.markerChoices = [shape for shape in self.valueLookup] #all shapes available in lookup dict
            self.markerChoice = tk.StringVar()
            self.markerOpt = ttk.OptionMenu(self, self.markerChoice, self.getCurrentMarker(), *self.markerChoices, command = self.setMarkerSelection)
            self.markerOpt.grid(column=1, row = 0, pady=10, padx=10,sticky=tk.EW)

            #Input widgets for defining marker color
            self.markerfacecolorLabel = ttk.Label(self, text='Fill Color: ')
            self.markerfacecolorLabel.grid(column=0, row=1, padx= 10, pady =10)

            self.markerfacecolorBtn = tk.Button(
                self, command= self.setMarkerFaceColor, bg= self.currentVals['markerfacecolor'],
                activebackground= self.currentVals['markerfacecolor'], width=5
            )
            self.markerfacecolorBtn.grid(column=1, row=1, padx=10, pady = 10)

            #Input widgets for defining marker outline color
            self.markeredgecolorLabel = ttk.Label(self, text='Outline Color: ')
            self.markeredgecolorLabel.grid(column=0, row=2, padx= 10, pady =10)

            self.markeredgecolorBtn = tk.Button(
                self, command= self.setMarkerEdgeColor, bg= self.currentVals['markeredgecolor'],
                activebackground= self.currentVals['markeredgecolor'], width=5
            )
            self.markeredgecolorBtn.grid(column=1, row=2, padx=10, pady = 10)

            #Input widgets for outline size
            self.markeredgewidthLabel = ttk.Label(self, text='Outline Width: ')
            self.markeredgewidthLabel.grid(column=0, row=3, padx= 10, pady =10)

            self.markeredgewidth = tk.IntVar( value= self.currentVals['markeredgewidth'])
            self.markeredgewidthSpin = ttk.Spinbox(self, from_= 0.0, to= 1000.0, textvariable=self.markeredgewidth)
            self.markeredgewidthSpin.grid(column=1, row=3, padx=10, pady = 10)

            #Input widgets for marker size
            self.markersizeLabel = ttk.Label(self, text='Size: ')
            self.markersizeLabel.grid(column=0, row=4, padx= 10, pady =10)

            self.markersize = tk.IntVar( value= self.currentVals['markersize'])
            self.markersizeSpin = ttk.Spinbox(self, from_= 0.0, to= 1000.0, textvariable=self.markersize)
            self.markersizeSpin.grid(column=1, row=4, padx=10, pady = 10)

            #Apply button
            self.applyBtn = ttk.Button(self, text='Apply', command=self.applySymbology)
            self.applyBtn.grid(column=0, columnspan= 2, row= 5, pady=10)
        except:
            ErrorDialog(f'Creating Point Symbology dialog for {self.layer}')

    def setMarkerSelection(self, choice):
        self.currentVals['marker'] = self.valueLookup[choice]

    def getCurrentMarker(self):
        current = self.currentVals['marker']
        invLookup = {v : k for k, v in self.valueLookup.items()}

        return invLookup[current]

    def setMarkerFaceColor(self):
        try:
            currentColor = self.currentVals['markerfacecolor']
            color = self.promptColor(currentColor)

            if color:
                self.currentVals['markerfacecolor'] = color[1]

                self.markerfacecolorBtn.configure({'bg': color[1], 'activebackground' : color[1]})
        except:
            ErrorDialog(f'Setting marker face color')

    def setMarkerEdgeColor(self):
        try:
            currentColor = self.currentVals['markeredgecolor']
            color = self.promptColor(currentColor)

            if color:
                self.currentVals['markeredgecolor'] = color[1]

                self.markeredgecolorBtn.configure({'bg': color[1], 'activebackground' : color[1]})
        except:
            ErrorDialog(f'Setting Marker Edge Color')

    def applySymbology(self):
        try:
            self.currentVals['markeredgewidth'] = self.markeredgewidth.get()
            self.currentVals['markersize'] = self.markersize.get()

            self.layer.pointSymbology = self.currentVals

            self.layer.redrawArtists()

            self.destroy()

        except:
            ErrorDialog(f'Applying new point symbology to {self.layer}')

class LineSymbolDialog(SymbolDialog):
    def __init__(self, layer):
        super().__init__(layer)

        self.title("Line Symbology Selector")

        self.nyiLabel = ttk.Label(self, text="This dialog has not been implemented yet")
        self.nyiLabel.pack(padx= 50, pady = 50)

class PolygonSymbolDialog(SymbolDialog):
    def __init__(self, layer):
        super().__init__(layer)

        self.title("Polygon Symbology Selector")

        self.nyiLabel = ttk.Label(self, text="This dialog has not been implemented yet")
        self.nyiLabel.pack(padx= 50, pady = 50)

class AttributeTable(tk.Toplevel):
    def __init__(self, layer):
        super().__init__()

        self.title(layer.name + " Layer Table")

        unavailable = ttk.Label(self, text='Layer tables have not yet been implemented...')
        unavailable.pack(pady=50,padx=50)

class ErrorDialog(tk.Toplevel):
    def __init__(self, msg = None):
        super().__init__()

        self.title("Uh-oh! A wild Error appeared.")
        self.attributes('-topmost', 'true')
        self.minsize(width= 200, height=300)

        self.description = ttk.Label(self, text= f"Error encountered while: {msg if msg else 'doing something unspecified'}")
        self.description.pack(side=tk.TOP,padx=15,pady=10)

        tb = exc_info()
        self.errorInfo = tk.Text(self, height= 10, width= 60)
        
        self.errorInfo.insert(1.0,"".join(format_exception(*tb)))
        self.errorInfo.configure(state = 'disabled')
        self.errorInfo.pack(side=tk.TOP, fill=tk.BOTH, pady=10, padx=15)

        self.close = ttk.Button(self, text='Close', command=self.destroy)
        self.close.pack(side=tk.TOP, pady=10)

        


