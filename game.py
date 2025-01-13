import numpy as np
import copy

class Board:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.grid = [[None for _ in range(columns)] for _ in range(rows)]
        self.memory = [0]
        self.history = [copy.deepcopy(self.grid)]

class Player:
    def __init__(self, color):
        self.color = color
        
    def __str__(self):
        return self.color

class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player('Red'), Player('Blue')]
        self.current_player = self.players[0]
        self.game_states = ['ongoing', 'win', 'draw'] 
        self.current_game_state = 'ongoing'

    def column_click(self, col_index):
        ## Iterate through the bins of the given column from top to bottom, insert a disc in the first
        ## available bin. If the entire column is full, do nothing
        for i in range(self.board.rows-1,-1,-1):
            if self.board.grid[i][col_index] == None:
                self.board.grid[i][col_index] = self.current_player.color
                self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
                self.board.memory.append(len(self.board.memory))
                
                ## Store the current game state in a history attribute
                self.board.history.append(copy.deepcopy(self.board.grid))

                ## Check for a win or a draw
                self.check_game()
                break

    def go_to_move(self, move_index):
        ## Modify the necessary changes once the players teleports to a previous move
        ## We will clear all the game info exceeding this move index and store the game board
        ## associated with the given move index to the current game board
        self.board.history = self.board.history[:move_index+1]
        self.board.memory = self.board.memory[:move_index+1]
        self.board.grid = copy.deepcopy(self.board.history[move_index])
        ## Alternative for determining who the current player was at that given move index
        ## is storing the players turns in the game history as well 
        self.current_player = self.players[0] if move_index % 2 == 0 else self.players[1]
    
    def new_game(self):
        ## Modify the necessary changes once the players start a new game
        self.board = Board()
        self.current_player = self.players[0]
        self.current_game_state = 'ongoing'
        return
    
    def check_game(self):
        ## Our strategy will be scanning all 4 diagonal and orthogonal bins in the game board
        ## We will store each combination of 4 given values in a list, and convert the list into a set
        ## Since a set stores only unique values, we are expected to notice a win if
        ## the set has only one element which is not None (either Blue or Red)
        x = np.array(self.board.grid)
        ## Iterate through board bins and look for a row, column and a diagonal
        for i in range(self.board.rows):
            for j in range(self.board.columns):
                x = np.array(self.board.grid)
                ## If a row of 4 bins starting in index i is inside the board bounds, check if theres a win
                if i < self.board.rows-3:
                    cur_column = set(x[i:i+4,j])
                    if len(cur_column) == 1 and None not in cur_column:
                        self.current_game_state = 'win'
                        break

                ## If a column of 4 bins starting in index ij is inside the board bounds, check if theres a win           
                if j < self.board.columns-3:
                    cur_row = set(x[i,j:j+4])
                    if len(cur_row) == 1 and None not in cur_row:
                        self.current_game_state = 'win'
                        break

                ## If a kernel of 4X4 bins starting in indices i, j is inside the board bounds, check if theres a win            
                if i < self.board.rows-3 and j < self.board.columns-3:
                    kernel = x[i:i+4, j:j+4]       
                    ## Retrieve the left and right diagonal elements of a given kernel and store them in a list
                    left_diag, right_diag = set(np.diag(kernel).tolist()), set(np.diag(np.fliplr(kernel)).tolist())
                    if (len(left_diag) == 1 and None not in left_diag) or (len(right_diag) == 1 and None not in right_diag):
                        self.current_game_state = 'win'
                        break
    
            if np.count_nonzero(x) == self.board.rows * self.board.columns:
                self.current_game_state = 'draw'

    ## Do not change this implememtation
    def to_dict(self):
        return {
            'grid': self.board.grid,
            'memory': self.board.memory,
            'players': [str(player) for player in self.players],
            'current_player': str(self.current_player),
            'game_states': self.game_states,
            'current_game_state': self.current_game_state
        }
