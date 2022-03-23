from PIL import ImageTk, Image


class Tile:
    def __init__(self, letter, pos: tuple, parent):  # (x, y)
        self.margin = parent.margin  # parent.margin
        self.side = parent.side
        self.letter = letter
        self.structure = None
        self.recessed_Tile = None
        self.parent = parent.canvas
        self.connections = 0
        self.pos = pos
        self.closed = False
        self.value = None
        self.image = None
        self.lettering = None
        # print( tkFont.families())

    def __str__(self):
        return self.letter

    def create_Tile_Gfx(self, board_Positions):  # pos[0] = xIdx, pos[1] = yIdx
        x_Offset = 35
        y_Offset = 40
        self.image = ImageTk.PhotoImage(Image.open('images/tile_Yellow.png').resize((self.side, self.side)))
        self.recessed_Tile = ImageTk.PhotoImage(Image.open('images/recessed_Tile_3.png').resize((self.side, self.side)))
        self.parent.create_image((self.pos[1] * self.side) + x_Offset, (self.pos[0] * self.side) + y_Offset,
                                 image=self.recessed_Tile)
        self.structure = self.parent.create_image((self.pos[1] * self.side) + x_Offset, (self.pos[0] * self.side) + y_Offset,
                                                  image=self.image)
        self.lettering = self.parent.create_text(self.pos[1] * self.side + x_Offset, self.pos[0] * self.side + y_Offset,
                                                 text=self.letter, font=self.parent.tile_Font)
        board_Positions[self.pos[0]][self.pos[1]] = self
