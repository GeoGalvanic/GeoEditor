import tkinter as tk

class AttributeDialog(tk.Toplevel):
    existingWindow = None

    def __init__(self):
        super().__init__()

        self.title(f' - Attributes')

        self.protocol("WM_DELETE_WINDOW", self.closeWindow)

    def closeWindow(self):
        AttributeDialog.existingWindow = None
        self.destroy()

    def openOrAdd():
        if AttributeDialog.existingWindow:
            label = tk.Label(AttributeDialog.existingWindow, text="Window already open...")
            label.grid(column=0,row=0)
        else:
            AttributeDialog.existingWindow = AttributeDialog()
