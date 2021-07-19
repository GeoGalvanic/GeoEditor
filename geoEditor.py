'''
Main script for initializing GeoEditor functions and UI.

Created by: Geal Q. Sarrett 08JUL21
'''

import matplotlib.pyplot as plt
import tkinter as tk
import logging
from geometryClasses import *
from menuGUI import *
from mplElements import GEFigure

root= tk.Tk()
root.title("GeoEditor")
root.option_add('*tearOff', tk.FALSE)
root['menu'] = GeoMenu(root)

figure = GEFigure(root)

plt.show(block=False)

root.mainloop()