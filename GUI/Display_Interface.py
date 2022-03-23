from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
from GUI.Board import call_Gameover


class Display_Interface:
    def __init__(self, parent, mode):
        self.interface_Font = tkFont.Font(family='Arial Rounded MT Bold', size=14, weight='bold')
        self.display_Font = tkFont.Font(family='Arial Rounded MT Bold', size=18, weight='bold')
        self.side = parent.side
        self.margin = parent.margin
        self.parent = parent.canvas
        self.interface_Image = ImageTk.PhotoImage(Image.open('images/btn_Orange_1.png').resize((100, 75)))
        self.mode = mode
        self.time_Label = None
        self.time_Label_Timer_ID = None
        self.tiles_Label = None
        self.score_Label = None
        self.opponent_Tiles_Label = None
        self.opponent_Score_Label = None
        self.opponent_Errors_Label = None
        self.recessed_Tile = None

    def init_Labels(self):
        self.time_Label = Label(self.parent, text='300', image=self.interface_Image, borderwidth=0,
                                bg='grey', compound='center', font=self.display_Font)
        self.time_Label.place(x=685, y=50)
        self.time_Label.x = 685
        self.time_Label.y = 50
        self.time_Label.width = 100
        self.time_Label.height = 75

        self.parent.create_text(self.time_Label.x + self.time_Label.width/2,
                                self.time_Label.y + self.time_Label.height+15, text='Time',
                                font=self.interface_Font)

        self.score_Label = Label(self.parent, text='0', image=self.interface_Image, borderwidth=0,
                                 bg='grey', compound='center', font=self.display_Font)
        self.score_Label.place(x=685, y=150)
        self.score_Label.x = 685
        self.score_Label.y = 150
        self.score_Label.width = 100
        self.score_Label.height = 75
        self.parent.create_text(self.score_Label.x + self.score_Label.width / 2,
                                self.score_Label.y + self.score_Label.height + 15, text='Score',
                                font=self.interface_Font)

        self.tiles_Label = Label(self.parent, text='24', anchor='n', image=self.interface_Image, borderwidth=0,
                                 bg='grey', compound='center', font=self.display_Font)
        self.tiles_Label.place(x=685, y=250)
        self.tiles_Label.x = 685
        self.tiles_Label.y = 250
        self.tiles_Label.width = 100
        self.tiles_Label.height = 75
        self.parent.create_text(self.tiles_Label.x + self.tiles_Label.width / 2,
                                self.tiles_Label.y + self.tiles_Label.height + 15, text='Tiles',
                                font=self.interface_Font)

    def init_Opponent_Labels(self):
        self.opponent_Errors_Label = Label(self.parent, text='0', anchor='n', image=self.interface_Image,
                                          borderwidth=0,
                                          bg='grey', compound='center', font=self.display_Font)
        self.opponent_Errors_Label.place(x=850, y=50)
        self.opponent_Errors_Label.x = 850
        self.opponent_Errors_Label.y = 50
        self.opponent_Errors_Label.width = 100
        self.opponent_Errors_Label.height = 75
        self.parent.create_text(self.opponent_Errors_Label.x + self.opponent_Errors_Label.width / 2,
                                self.opponent_Errors_Label.y + self.opponent_Errors_Label.height + 15, text='Errors',
                                font=self.interface_Font)

        self.opponent_Score_Label = Label(self.parent, text='0', image=self.interface_Image, borderwidth=0,
                                 bg='grey', compound='center', font=self.display_Font)
        self.opponent_Score_Label.place(x=850, y=150)
        self.opponent_Score_Label.x = 850
        self.opponent_Score_Label.y = 150
        self.opponent_Score_Label.width = 100
        self.opponent_Score_Label.height = 75
        self.parent.create_text(self.opponent_Score_Label.x + self.opponent_Score_Label.width / 2,
                                self.opponent_Score_Label.y + self.opponent_Score_Label.height + 15, text='Score',
                                font=self.interface_Font)

        self.opponent_Tiles_Label = Label(self.parent, text='24', anchor='n', image=self.interface_Image, borderwidth=0,
                                 bg='grey', compound='center', font=self.display_Font)
        self.opponent_Tiles_Label.place(x=850, y=250)
        self.opponent_Tiles_Label.x = 850
        self.opponent_Tiles_Label.y = 250
        self.opponent_Tiles_Label.width = 100
        self.opponent_Tiles_Label.height = 75
        self.parent.create_text(self.opponent_Tiles_Label.x + self.opponent_Tiles_Label.width / 2,
                                self.opponent_Tiles_Label.y + self.opponent_Tiles_Label.height + 15, text='Tiles',
                                font=self.interface_Font)

    def init_Opponent_Swap_Bar(self):
        x_Offset = 35
        y_Offset = 45
        self.recessed_Tile = ImageTk.PhotoImage(Image.open('images/recessed_Tile_3.png').resize((50, 50)))
        for xIdx in range(16, 19):
            self.parent.create_image((xIdx * self.side) + x_Offset, (7 * self.side) + y_Offset,
                                     image=self.recessed_Tile)

    def countdown(self, count):
        if count >= 0:
            self.time_Label.config(text=count)
            self.time_Label_Timer_ID = self.parent.after(1000, self.countdown, count - 1)
        else:
            self.parent.after_cancel(self.time_Label_Timer_ID)
            call_Gameover(self.parent)

    def set_Score_Label(self, score):
        print(f'Setting Score: {score}')
        self.score_Label.config(text=score)

    def set_Tiles_Label(self):
        aux_Tiles_Remaining = int(self.tiles_Label.cget('text')) - 1
        self.tiles_Label.config(text=aux_Tiles_Remaining)
