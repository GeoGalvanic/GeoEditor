import dialogGUI
from layerClasses import Layer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

class GEFigure(plt.Figure):
    figures = [] #List of active figures

    def __init__(self, parent):
        super().__init__()

        self.subplot = self.add_subplot()
        self.subplot.set_axis_off()
        self.subplot.set_aspect('equal', adjustable = 'datalim', anchor = 'C')

        self.canvas = FigureCanvasTkAgg(self, parent)

        self.set_tight_layout(True)

        self.canvas.mpl_connect('pick_event', self.on_pick)
        toolbar = NavigationToolbar2Tk(self.canvas, parent, pack_toolbar=False)
        toolbar.update()

        toolbar.pack(side=tk.TOP,fill=tk.X)
        self.canvas.get_tk_widget().pack(expand = True, side=tk.TOP, fill=tk.BOTH)

        self.figures.append(self)

    def on_pick(self, event):
        if event.mouseevent.name == 'button_press_event':
            for layer in Layer.activeLayers:
                try:
                    dialogGUI.AttributeDialog.openOrAdd(layer.artistEntityPairs[event.artist])
                except KeyError:
                    pass
