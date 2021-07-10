'''
Main script for initializing GeoEditor functions and UI.

Created by: Geal Q. Sarrett 08JUL21
'''

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import geopandas as gpd
import tkinter as tk
from tkinter import ttk
import logging
from geometryClasses import *

def on_pick(event):
    print(event.artist)
    print(event.artist.properties())
    print(event.artist.contains(event.mouseevent))


world = gpd.read_file("../Lesson2/Data/funshape.shp")

print(world.geometry)

root= tk.Tk() 
  
figure1 = plt.Figure()

ax1 = figure1.add_subplot()
ax1.set_axis_off()
#ax1.set_picker(5)
canvas = FigureCanvasTkAgg(figure1, root)
figure1.tight_layout()

canvas.get_tk_widget().pack(expand = True, side=tk.TOP, fill=tk.BOTH)

entityList = []
artistList = []
for i, row in world.iterrows():
    print(row)
    entity = PolygonEntity(row)
    entityList.append(entity)

for entity in entityList:
    for patch in entity.patches:
        artist = ax1.add_patch(patch)
        artistList.append(artist)



figure1.canvas.mpl_connect('pick_event', on_pick)

plt.show(block=False)
#canvas.draw()

#for artist in artistList:
#     ax1.draw_artist(artist)

ax1.autoscale()


root.mainloop()