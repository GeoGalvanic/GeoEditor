'''
Main script for initializing GeoEditor functions and UI.

Created by: Geal Q. Sarrett 08JUL21
'''

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import geopandas as gpd
import tkinter as tk
import logging
from geometryClasses import *
from layerClasses import Layer
from dialogGUI import *

def on_pick(event):
    if event.mouseevent.name == 'button_press_event':
        print(layer.artistEntityPairs[event.artist].gdfRow)
        AttributeDialog.openOrAdd()

root= tk.Tk()
root.title("GeoEditor")
  
figure1 = plt.Figure()

ax1 = figure1.add_subplot()
ax1.set_axis_off()

canvas = FigureCanvasTkAgg(figure1, root)
figure1.tight_layout()

canvas.get_tk_widget().pack(expand = True, side=tk.TOP, fill=tk.BOTH)

layer = Layer("../Lesson2/Data/funshape.shp", ax1)

figure1.canvas.mpl_connect('pick_event', on_pick)

plt.show(block=False)

ax1.autoscale()


root.mainloop()