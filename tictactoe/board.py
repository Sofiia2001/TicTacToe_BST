# Module from Oles' consultation

import random
import copy


def generate_winning_combinations():
    '''
    Function that generates all possible winning combinations

    :return: list of combinations
    '''
    combinations = []
    for i in range(3):
        combination1 = []
        combination2 = []
        for j in range(3):
            combination1.append((i, j))
            combination2.append((j, i))
        combinations.append(combination1)
        combinations.append(combination2)

    combinations.append([(0, 0), (1, 1), (2, 2)])
    combinations.append([(0, 2), (1, 1), (2, 0)])
    return combinations


class Board:
    '''
    Class that represents a game board
    '''
    NOUGHT = 1
    CROSS = -1
    EMPTY = 0

    NOUGHT_WINNER = 1
    CROSS_WINNER = -1
    DRAW = 2
    NOT_FINISHED = 0

    WINNING_COMBINATIONS = generate_winning_combinations()

    def __init__(self):
        '''
        Initializes variables, generates cells
        '''
        self.cells = [[0] * 3 for _ in range(3)]
        self.last_move = 1
        self.number_of_moves = 0

    def make_move(self, cell):
        '''
        Makes a move on a specific place on a board

        :param cell: tuple of integers
        :return: bool
        '''
        if self.cells[cell[0]][cell[1]] != 0:
            return False

        self.last_move = - self.last_move
        self.cells[cell[0]][cell[1]] = self.last_move
        self.number_of_moves += 1
        return True

    def has_winner(self):
        '''
        Method to check if someone wins the game or no one wins

        :return: int
        '''
        for combination in self.WINNING_COMBINATIONS:
            lst = []
            for cell in combination:
                lst.append(self.cells[cell[0]][cell[1]])
            if max(lst) == min(lst) and max(lst) != Board.EMPTY:
                return max(lst)

        if self.number_of_moves == 9:
            return Board.DRAW

        return Board.NOT_FINISHED

    def make_random_move(self):
        '''
        Makes a random move for future tree building

        :return: bool
        '''
        possible_moves = []
        for i in range(3):
            for j in range(3):
                if self.cells[i][j] == Board.EMPTY:
                    possible_moves.append((i, j))
        if possible_moves:
            cell = random.choice(possible_moves)
            self.last_move = - self.last_move
            self.cells[cell[0]][cell[1]] = self.last_move
            self.number_of_moves += 1
            return True

    def __str__(self):
        '''
        String representation of a board

        :return: str
        '''
        transform = {0: ' ', 1: 'O', -1: 'X'}
        return '\n'.join([' '.join(map(lambda x: transform[x], row)) for row in self.cells])

