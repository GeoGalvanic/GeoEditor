'''
Main script for initializing GeoEditor functions and UI.

Created by: Geal Q. Sarrett 08JUL21
'''

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import geopandas as gpd
import tkinter as tk
import logging
from geometryClasses import *
from layerClasses import Layer
from dialogGUI import *

def on_pick(event):
    if event.mouseevent.name == 'button_press_event':
        for layer in Layer.activeLayers:
            try:
                AttributeDialog.openOrAdd(layer.artistEntityPairs[event.artist])
            except KeyError:
                pass

root= tk.Tk()
root.title("GeoEditor")
  
figure1 = plt.Figure()
ax1 = figure1.add_subplot()
ax1.set_axis_off()
figure1.tight_layout()


canvas = FigureCanvasTkAgg(figure1, root)

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

toolbar.pack(side=tk.TOP,fill=tk.X)
canvas.get_tk_widget().pack(expand = True, side=tk.TOP, fill=tk.BOTH)

layer = Layer("../Lesson2/Data/countries.shp", ax1, displayField="NAME")
layer2  = Layer("../Lesson2/Data/pointsInCountry.shp", ax1)
layer2  = Layer("../Lesson2/Data/randomlines.shp", ax1)

figure1.canvas.mpl_connect('pick_event', on_pick)

plt.show(block=False)

ax1.autoscale()
ax1.set_aspect('equal', adjustable = 'datalim', anchor = 'C')

root.mainloop()