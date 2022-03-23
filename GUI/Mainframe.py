import tkinter.font as tkFont
from tkinter import *


class Mainframe:
    def __init__(self):

        self.root = Tk()
        self.root.geometry('800x500')  # 800x500
        self.root.title('Hello Words')
        self.canvas = Canvas(self.root,
                             width=1000,
                             height=500,
                             bg='grey')
        self.side = 50
        self.margin = 10
        self.canvas.create_rectangle(0, 365, 800, 500, width=4, fill='slate gray')
        self.canvas.grid(column=0, row=0, columnspan=14)
        self.canvas.tile_Font = tkFont.Font(family='Arial Rounded MT Bold', size=24, weight='bold')
        self.canvas.parent = self.root
