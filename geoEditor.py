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

def on_pick(event):
    print(event.artist)
    print(event.artist.properties())
    print(event.ind)
    print(event.artist.contains(event.mouseevent))
    for i in event.ind:
        print(world.iloc[i])


world = gpd.read_file("../Lesson2/Data/funshape.shp")

print(world.head())

root= tk.Tk() 
  
figure1 = plt.Figure()

ax1 = figure1.add_subplot()
ax1.set_axis_off()
#ax1.set_picker(5)
canvas = FigureCanvasTkAgg(figure1, root)
figure1.tight_layout()



canvas.get_tk_widget().pack(expand = True, side=tk.TOP, fill=tk.BOTH)
world.plot(ax=ax1, picker=True)

figure1.canvas.mpl_connect('pick_event', on_pick)


root.mainloop()