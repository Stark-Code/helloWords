from tkinter import *
import logic
from PIL import ImageTk, Image
from GUI.Tile import Tile
import math


def call_Gameover(parent):
    print('Good Game!')
    parent.unbind("<B1-Motion>")
    parent.unbind('<Button-1>')
    parent.unbind('<ButtonRelease-1>')
    parent.submit_Btn.config(state='disabled')


class Board:
    def __init__(self, parent, display_Interface, aux_Tiles):

        self.display_Interface = display_Interface

        self.margin = parent.margin
        self.side = parent.side  # cell dimension
        self.width = self.margin * 2 + self.side * 13
        self.height = self.margin * 2 + self.side * 7
        self.offset_Y = 35
        self.offset_X = 35

        self.parent = parent
        self.parent.canvas.bind("<B1-Motion>", self.move)
        self.parent.canvas.bind('<Button-1>', self.grab)
        self.parent.canvas.bind('<ButtonRelease-1>', self.drop)

        self.has_Tile = False
        self.tile = None
        self.aux_Tiles = aux_Tiles

        self.bg_Images = []  # Prevents garbage collector from deleting bg resources
        self.submit_Btn_Image = ImageTk.PhotoImage(Image.open('images/play_Btn_Orange_1.png').resize((100, 100)))

        self.board = [[0 for x in range(13)] for y in range(9)]
        self.opponent_Swap_Bar = [0, 0, 0]

        self.tile_Count = 26
        self.row, self.col = 0, 0

    def get_Aux_Tile(self):
        self.tile_Count += 1
        self.display_Interface.set_Tiles_Label()
        new_Tile = Tile(self.aux_Tiles.pop(), (7, 0), self.parent)  # mainframe.mainframe
        new_Tile.create_Tile_Gfx(self.board)

    def submit(self):
        # print(f'Test {self.display_Interface.tiles_Label.cget("text")}')
        words_Found, incorrect_Word_Positions, path_Start, tiles_On_Board = logic.find_Words(self.board)
        if incorrect_Word_Positions:
            self.mark_Errors(incorrect_Word_Positions)
            return
        legal_Board = logic.check_Connectivity(self.board, path_Start, tiles_On_Board)
        if legal_Board:
            length_Score = logic.calculate_Length_Score(words_Found)
            double_Score = logic.calculate_Double_Tile_Score(self.board)
            self.display_Interface.set_Score_Label(length_Score + double_Score)
            if tiles_On_Board == self.tile_Count:
                if len(self.aux_Tiles) > 0:
                    self.get_Aux_Tile()
                else:
                    self.parent.canvas.after_cancel(self.display_Interface.time_Label_Timer_ID)
                    call_Gameover(self.parent.canvas)
        else:
            self.mark_Disconnected()

    def redraw_Tile(self, current_Tile, x, y):
        self.parent.canvas.delete(current_Tile.structure)
        current_Tile.structure = self.parent.canvas.create_image(x, y, image=current_Tile.image)
        self.parent.canvas.delete(current_Tile.lettering)
        current_Tile.lettering = self.parent.canvas.create_text(x, y, font=self.parent.canvas.tile_Font, text=current_Tile.letter)

    def grab(self, e):
        row, col = math.floor((e.y - self.margin) / self.side), math.floor((e.x - self.margin) / self.side)
        print(f'Row/Col: {row, col}')

        if row < 0 or row > 8: return
        if col < 0 or col > 12: return
        if not isinstance(self.board[row][col], Tile): return
        print('grab')
        self.tile = self.board[row][col]
        self.board[row][col] = 0
        self.has_Tile = True

    def drop(self, e):
        row, col = math.floor((e.y - self.margin) / self.side), math.floor((e.x - self.margin) / self.side)
        print(f'Row/Col: {row, col}')

        if not self.has_Tile: return

        if row == 7 and col in [16, 17, 18]:  # Opponent Swap Bar
            col_Idx = [16, 17, 18].index(col)
            if self.opponent_Swap_Bar[col_Idx] == 0:
                self.tile.pos = (row, col)
                self.redraw_Tile(self.tile, (self.tile.pos[1] * self.side) + self.offset_X,
                                 (self.tile.pos[0] * self.side) + self.offset_Y)
                self.opponent_Swap_Bar[col_Idx] = self.tile
            else:
                self.redraw_Tile(self.tile, (self.tile.pos[1] * self.side) + self.offset_X,
                                 (self.tile.pos[0] * self.side) + self.offset_Y)
                self.board[self.tile.pos[0]][self.tile.pos[1]] = self.tile
            self.has_Tile = False
            return

        if row > 8 or row < 0 or col > 12 or col < 0:  # Prevents error if tile is dragged to edges of board and dropped
            self.redraw_Tile(self.tile, (self.tile.pos[1] * self.side) + self.offset_X, (self.tile.pos[0] * self.side) + self.offset_Y)
            self.board[self.tile.pos[0]][self.tile.pos[1]] = self.tile
            self.has_Tile = False
            return

        if self.board[row][col] == 0:
            self.board[row][col] = self.tile
            self.tile.pos = (row, col)
            self.redraw_Tile(self.tile, (self.tile.pos[1] * self.side) + self.offset_X, (self.tile.pos[0] * self.side) + self.offset_Y)

        elif isinstance(self.board[row][col], Tile):
            print(f'y: {self.tile.pos[0]},x: {self.tile.pos[1]}')

            swap_Tile = self.board[row][col]
            self.board[self.tile.pos[0]][self.tile.pos[1]] = swap_Tile
            swap_Tile.pos = self.tile.pos
            self.redraw_Tile(swap_Tile, (swap_Tile.pos[1] * self.side) + self.offset_X, (swap_Tile.pos[0] * self.side) + self.offset_Y)

            self.board[row][col] = self.tile
            self.tile.pos = (row, col)
            self.redraw_Tile(self.tile, (self.tile.pos[1] * self.side) + self.offset_X, (self.tile.pos[0] * self.side) + self.offset_Y)

        self.has_Tile = False

    def move(self, e):
        if not self.has_Tile: return
        self.redraw_Tile(self.tile, e.x, e.y)

    def draw_Grid_BG(self):
        for y in range(13):  # Row
            y_Pos = self.margin + y * self.side
            for x in range(7):  # Column
                x_Pos = self.margin + x * self.side
                board_Image = ImageTk.PhotoImage(Image.open('images/board_Cartoon_Fitted.png').resize((self.side, self.side)))
                self.bg_Images.append(board_Image)
                self.parent.canvas.create_image(y_Pos, x_Pos, anchor='nw', image=board_Image)

    def draw_Grid(self):
        for y in range(14):
            x0 = self.margin + y * self.side  # Column
            y0 = self.margin
            x1 = self.margin + y * self.side
            y1 = self.height - self.margin
            self.parent.canvas.create_line(x0, y0, x1, y1, width=10, fill='black', capstyle='round')

        for x in range(8):
            x0 = self.margin  # Row
            y0 = self.margin + x * self.side
            x1 = self.width - self.margin
            y1 = self.margin + x * self.side
            self.parent.canvas.create_line(x0, y0, x1, y1, width=10, fill='black', capstyle='round')

    def mark_Errors(self, incorrect_Word_Positions):
        for word_Pos in incorrect_Word_Positions:
            for tile_Pos in word_Pos:
                tile = self.board[tile_Pos[0]][tile_Pos[1]]
                tile.image = ImageTk.PhotoImage(Image.open('images/tile_Flame.png').resize((self.side, self.side)))
                self.redraw_Tile(tile, (tile_Pos[1] * self.side) + 35, (tile_Pos[0] * self.side) + 35)


    def mark_Disconnected(self):
        print('Disconnected word/s on board')
        for row_Idx in range(len(self.board) - 2):
            for col_Idx in range(len(self.board[row_Idx])):
                if isinstance(self.board[row_Idx][col_Idx], Tile):
                    tile = self.board[row_Idx][col_Idx]
                    if not tile.closed:
                        tile.image = ImageTk.PhotoImage(Image.open('images/tile_Iced_2.png').resize((self.side, self.side)))
                        self.redraw_Tile(tile, (col_Idx * self.side) + 35, (row_Idx * self.side) + 35)
