from board import Board
from linked_binary_tree import LinkedBinaryTree
import copy


class TicTacToeTree:
    '''
    Class to represent TicTacToe game with computer
    '''
    def __init__(self, root):
        '''
        Initializes variables including root of a future generated tree

        :param root: Board
        '''
        self.root = root
        self.tree = LinkedBinaryTree(root)

    def generate_tree(self, root=None):
        '''
        Generates a binary search tree of possible choices

        :param root: Board
        :return: None
        '''
        if root is None: root = self.tree
        else: root = root
        if root.key.has_winner():
            return 0
        right_board = copy.deepcopy(root.key)
        left_board = copy.deepcopy(root.key)
        right_board.make_random_move()
        left_board.make_random_move()

        root.insert_left(left_board)
        root.insert_right(right_board)

        self.generate_tree(root.left_child)
        self.generate_tree(root.right_child)
        return

    def count_winning_amount(self):
        '''
        Counts amount of winning combinations on both sides of a tree

        :return: (int, int)
        '''
        my_tree = self.tree
        right_tree = my_tree.right_child
        left_tree = my_tree.left_child
        right_counter = set()
        left_counter = set()
        right_nodes = right_tree.get_leaves_list()
        left_nodes = left_tree.get_leaves_list()

        for right in right_nodes:
            if right.has_winner() == right.CROSS:
                right_counter.add(str(right))

        for left in left_nodes:
            if left.has_winner() == left.CROSS:
                left_counter.add(str(left))

        return len(right_counter), len(left_counter)


def main():
    '''
    Main function to simulate a Tic Tac Tie game

    :return: None
    '''
    transform = {1: 'NOUGHT', -1: 'CROSS', 2: 'DRAW'}
    init_board = Board()
    init_board.make_random_move()
    while True:
        if init_board.has_winner():
            print(init_board)
            print(f'And the winner is: {transform[init_board.has_winner()]}')
            break

        print(init_board)
        while True:
            user_choice = input('Enter your choice[1 1]: ')
            try:
                splitted = [int(i) for i in user_choice.split()]
                assert 0 <= splitted[0] <= 2
                assert 0 <= splitted[1] <= 2
                assert init_board.cells[splitted[0]][splitted[1]] == 0
                break

            except:
                print('Wrong choice')
                continue

        init_board.make_move(splitted)

        tic = TicTacToeTree(init_board)
        tic.generate_tree()
        tree_winning_combinations = tic.count_winning_amount()
        right_subtree = tree_winning_combinations[0]
        left_subtree = tree_winning_combinations[1]
        init_board = tic.tree.left_child.key
        if right_subtree >= left_subtree: init_board = tic.tree.right_child.key


if __name__ == '__main__':
    main()