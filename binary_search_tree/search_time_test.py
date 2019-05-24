import time
import random
from linkedbst import LinkedBST
import sys


sys.setrecursionlimit(500000)


def read_from_dictionary():
    '''
    Reads a file with english dictionary

    :return: list of words
    '''
    with open('words.txt') as dictionary:
        lines = dictionary.readlines()

    words_list = [line.strip() for line in lines]
    return words_list


def time_search_list(words, dictionary):
    '''
    Calculates a working time of a search in python list

    :param words: list
    :param dictionary: list
    :return: float work time
    '''
    curr = time.time()
    for w in words: dictionary.index(w)
    return round(time.time() - curr, 3)


def time_search_bst(words, dictionary):
    '''
    Calculates a working time of a search in a binary search tree

    :param words: list
    :param dictionary: list
    :return: float work time
    '''
    curr = time.time()
    dictionary = random.shuffle(dictionary)
    tree = LinkedBST(dictionary)
    for w in words: tree.find(w)
    return round(time.time() - curr, 3)


def time_search_balanced_bst(words, dictionary):
    '''
    Calculates a working time of a search in rebalanced binary search tree

    :param words: list
    :param dictionary: list
    :return: float work time
    '''
    curr = time.time()
    dictionary = random.shuffle(dictionary)
    tree = LinkedBST(dictionary)
    tree.rebalance()
    for w in words: tree.find(w)
    return round(time.time() - curr, 3)


def main():
    '''
    Main function to reflect the results

    :return: None
    '''
    dictionary = read_from_dictionary()
    WORDS = []
    for _ in range(10000):
        w = random.choice(dictionary)
        if w not in WORDS: WORDS.append(w)

    print(f'Working time of search in a '
          f'python list: {time_search_list(WORDS, dictionary)} seconds')

    print(f'Working time of search in a binary '
          f'search tree: {time_search_bst(WORDS, dictionary)} seconds')

    print(f'Working time of search in a balanced '
          f'binary search tree: {time_search_balanced_bst(WORDS, dictionary)} seconds')


if __name__ == '__main__':
    main()