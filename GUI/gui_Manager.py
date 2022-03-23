from GUI.Board import Board
from GUI.Mainframe import Mainframe
from GUI.Tile import Tile
from GUI.Display_Interface import Display_Interface
from GUI.game_Mode_Interface import Game_Mode_Interface
from logic import letter_Generator
from PIL import ImageTk, Image
from tkinter import Button


def select_Game_Mode():
    mainframe = Mainframe()
    game_Mode_Interface = Game_Mode_Interface(mainframe, start_Game)
    game_Mode_Interface.init_Buttons()
    game_Mode_Interface.init_Labels()
    mainframe.root.mainloop()


def start_Game(mainframe, mode, db_Table_Ref):
    # mainframe = Mainframe()
    if mode == 'multi':
        mainframe.root.geometry('1000x500')
        mainframe.canvas.create_line(800, 0, 800, 500, width=4, fill='black', capstyle='round')

    display_Interface = Display_Interface(mainframe, mode)
    display_Interface.init_Labels()
    if mode == 'multi':
        display_Interface.init_Opponent_Labels()
        display_Interface.init_Opponent_Swap_Bar()

    display_Interface.countdown(300)

    starting_Tiles, aux_Tiles = letter_Generator()

    game_Board = Board(mainframe, display_Interface, aux_Tiles)
    game_Board.draw_Grid()
    game_Board.draw_Grid_BG()

    submit_Btn = Button(mainframe.canvas, text="Submit", highlightthickness=0, activebackground='slate gray',
                        bg='slate gray', image=game_Board.submit_Btn_Image, borderwidth=0, command=game_Board.submit)
    submit_Btn.place(x=685, y=380)
    mainframe.canvas.submit_Btn = submit_Btn

    for yIdx in range(7, 9):
        for xIdx in range(13):
            new_Tile = Tile(starting_Tiles[yIdx-7][xIdx], (yIdx, xIdx), mainframe)  # mainframe.mainframe
            new_Tile.create_Tile_Gfx(game_Board.board)

    # mainframe.root.mainloop()
