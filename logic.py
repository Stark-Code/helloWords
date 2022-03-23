import GUI.Board
import random
with open('./word_List/Collins Scrabble Words (2019).txt') as f:
    word_Index = f.read().splitlines()


def letter_Generator():
    random_Index = [i for i in range(100)]
    random.shuffle(random_Index)

    letters = ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
               'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T',
               'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
               'I', 'I', 'I', 'I', 'I', 'I',
               'N', 'N', 'N', 'N', 'N', 'N', 'N',
               'O', 'O', 'O', 'O', 'O', 'O', 'O',
               'S', 'S', 'S', 'S', 'S', 'S',
               'H', 'H', 'H', 'H', 'H', 'H',
               'R', 'R', 'R', 'R', 'R', 'R',
               'D', 'D', 'D', 'D',
               'L', 'L', 'L', 'L',
               'U', 'U', 'U',
               'C', 'C', 'C',
               'M', 'M', 'M',
               'F', 'F',
               'W', 'W',
               'Y', 'Y',
               'G', 'G',
               'P', 'P',
               'B', 'B',
               'V', 'K', 'Q', 'J', 'X', 'Z']

    random_Letters = [[], []]
    aux_Letters = []

    for i in range(13):
        random_Letters[0].append(letters[random_Index[i]])

    for i in range(13, 26):
        random_Letters[1].append(letters[random_Index[i]])

    for i in range(26, 50):
        aux_Letters.append(letters[random_Index[i]])

    starting_Tiles = [random_Letters[0], random_Letters[1]]
    return starting_Tiles, aux_Letters


def check_Word(word, word_Positions, word_List):
    word_Found = False
    if len(word) > 1:
        print(f'Checking Word: {word}')
        if word in word_Index:
            word_Found = True
            word_List.append(word)
        else:
            print(f'{word} not found in dictionary')
            return word_List, word_Positions, word_Found
    return word_List, None, word_Found


def update_Tile_Connections(board, tile_Positions, origin):  # For calculating double tile scores
    for position in tile_Positions:
        tile = board[position[0]][position[1]]
        tile.connections += 1
        print(origin)
        # print(f'Tile {tile.letter} has {tile.connections} connection')


def find_Words(board):  # Scan Horizontally and Vertically
    tiles_On_Board = 0
    path_Start = None
    word_List = []
    incorrect_Word_Positions = []

    for row_Idx in range(len(board)-2):
        h_Word = ''
        h_Word_Positions = []
        for col_Idx in range(len(board[row_Idx])):
            if isinstance(board[row_Idx][col_Idx], GUI.Board.Tile):  # Horizontal
                tile = board[row_Idx][col_Idx]
                tiles_On_Board += 1
                tile.closed = False  # Reopen nodes closed in previous connection test
                tile.connections = 0
                if path_Start is None:
                    path_Start = [row_Idx, col_Idx]
                    tile.closed = True  # Prevent cyclic connectivity check
                h_Word += tile.letter
                h_Word_Positions.append((row_Idx, col_Idx))
            else:
                word_List, incorrect_Locations, word_Found = check_Word(h_Word, h_Word_Positions, word_List)
                if incorrect_Locations:
                    incorrect_Word_Positions.append(incorrect_Locations)
                elif word_Found:
                    update_Tile_Connections(board, h_Word_Positions, 'Horizontal First')
                h_Word = ''
                h_Word_Positions = []
        word_List, incorrect_Locations, word_Found = check_Word(h_Word, h_Word_Positions, word_List)
        if incorrect_Locations:
            incorrect_Word_Positions.append(incorrect_Locations)
        elif word_Found:
            update_Tile_Connections(board, h_Word_Positions, 'Horizontal Last')

    for col_Idx in range(len(board[0])):
        v_Word = ''
        v_Word_Positions = []
        for row_Idx in range(len(board)-2):  # Exiting loop without checking/adding word
            if isinstance(board[row_Idx][col_Idx], GUI.Board.Tile):  # Vertical
                tile = board[row_Idx][col_Idx]
                v_Word += tile.letter
                v_Word_Positions.append((row_Idx, col_Idx))
            else:
                word_List, incorrect_Locations, word_Found = check_Word(v_Word, v_Word_Positions, word_List)
                if incorrect_Locations:
                    incorrect_Word_Positions.append(incorrect_Locations)
                elif word_Found:
                    update_Tile_Connections(board, v_Word_Positions, 'Vertical First')
                v_Word = ''
                v_Word_Positions = []  # Might Cause Errors?
        word_List, incorrect_Locations, word_Found = check_Word(v_Word, v_Word_Positions, word_List)
        if incorrect_Locations:
            incorrect_Word_Positions.append(incorrect_Locations)
        elif word_Found:
            update_Tile_Connections(board, v_Word_Positions, 'Vertical Last')

    print(word_List)

    return word_List, incorrect_Word_Positions, path_Start, tiles_On_Board


def calculate_Length_Score(word_List):
    length_Score = 0
    for word in word_List:
        word_Score = 0
        for i in range(1, len(word)+1):
            word_Score += i
        length_Score += word_Score
    return length_Score


def calculate_Double_Tile_Score(board):
    double_Score = 0
    for row in board:
        for tile in row:
            if isinstance(tile, GUI.Board.Tile):
                if tile.connections == 2:
                    double_Score += 10
    return double_Score


def check_Connectivity(board, path_Start, tiles_On_Board):
    # print(f'Path Start: {path_Start}')
    # print(f'Tiles on Board: {tiles_On_Board}')

    def recursive_DFS(node_Pos, board, tiles_On_Board):
        nonlocal visited
        # print(f'Visited: {visited}')
        if visited == tiles_On_Board:  # Examined every tile on board
            print('Valid Board')
            return True
        parent_Tile = board[node_Pos[0]][node_Pos[1]]
        for next_Pos in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
            # print(f'Search pos: {node_Pos[0] + next_Pos[0]}, {node_Pos[1] + next_Pos[1]}')
            search_Pos = [node_Pos[0] + next_Pos[0], node_Pos[1] + next_Pos[1]]
            if 0 <= search_Pos[0] < len(board)-2 and 0 <= search_Pos[1] < len(board[0]):
                candidate = board[search_Pos[0]][search_Pos[1]]
            else:
                continue
            if isinstance(candidate, GUI.Board.Tile) and not \
                    candidate.closed:
                visited += 1
                candidate.closed = True
                # print(f'Tile Visited: {candidate.letter} @ {search_Pos}')
                valid_Board = recursive_DFS(candidate.pos, board, tiles_On_Board)
                if valid_Board: return True
        return False

    if path_Start is not None:  # At least 1 tile on board
        board[path_Start[0]][path_Start[1]].closed = True
        visited = 1
        return recursive_DFS(path_Start, board, tiles_On_Board)
