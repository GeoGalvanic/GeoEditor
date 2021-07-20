'''
Main script for initializing GeoEditor functions and UI.

Created by: Geal Q. Sarrett 08JUL21
'''

import matplotlib.pyplot as plt
import tkinter as tk
from menuGUI import *
from mplElements import GEFigure
from dialogGUI import ErrorDialog

try:
    #Initialize the root tk app and set parameters
    root= tk.Tk()
    root.title("GeoEditor")
    root.option_add('*tearOff', tk.FALSE)

    #Add menubar and custom matplotlib figure to the application

    root['menu'] = GeoMenu(root)
    figure = GEFigure(root)

    plt.show(block=False)
except:
    ErrorDialog('Initializing script')

root.mainloop()