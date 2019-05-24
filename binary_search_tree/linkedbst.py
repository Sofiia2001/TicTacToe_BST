# GitHub resources were used to implement correctly all methods

"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log, log2, ceil


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height_helper(root, curr_level):
            '''
            Helper function
            :param top:
            :return:
            '''

            left_level, right_level = curr_level, curr_level
            if root.left is not None:
                left_level = height_helper(root.left, curr_level + 1)
            if root.right is not None:
                right_level = height_helper(root.right, curr_level + 1)
            return max(left_level, right_level)

        return height_helper(self._root, 0)

    def isBalanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() <= ceil(log(len(self) + 1, 2)) - 1

    def rangeFind(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return [item for item in self.inorder() if item >=low and item <= high]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        inorder_tree = list(self.inorder())
        self.clear()

        def create_balanced_BST(arr):
            if len(arr) == 0:
                return None

            middle = len(arr) // 2

            new_root = BSTNode(data=arr[middle])
            new_root.left = create_balanced_BST(arr[:middle])
            new_root.right = create_balanced_BST(arr[middle + 1:])

            return new_root

        self._root = create_balanced_BST(inorder_tree)
        self._size = len(inorder_tree)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        if not self.isBalanced():
            self.rebalance()

        # Less efficient O(n) but more understandable

        # larger_items = [tree_item for tree_item in self.inorder() if tree_item > item]
        # if len(larger_items) > 0:
        #     return min(larger_items)
        # else:
        #     return None

        # Next variant is more efficient solution O(log(n)) but less understandable

        node = self._root
        succ_node = None

        while node is not None:
            if item == node.data:
                break
            elif item < node.data:
                if succ_node is None or node.data < succ_node.data:
                    succ_node = node
                node = node.left
            else:
                node = node.right

        if node is None:
            if succ_node is not None:
                return succ_node.data
            return None

        # found node of with data equal to item
        if node.right is not None:
            # try to find the smallest node in the right subtree
            node = node.right
            while node.left is not None:
                node = node.left
            if succ_node is None:
                succ_node = node
            elif node.data < succ_node.data:
                succ_node = node
        elif succ_node is None:
            return None

        return succ_node.data

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        if not self.isBalanced():
            self.rebalance()

        # Less efficient O(n) more understandable

        # smaller_items = [tree_item for tree_item in self.inorder() if tree_item < item]
        # if len(smaller_items) > 0:
        #     return max(smaller_items)
        # else:
        #     return None

        # Next variant is more efficient solution O(log(n)) but less understandable
        node  = self._root
        pred_node = None

        while node is not None:
            if item == node.data:
                break
            elif item < node.data:
                node = node.left
            else:
                if pred_node is None or node.data > pred_node.data:
                    pred_node = node
                node = node.right

        if node is None:
            if pred_node is not None:
                return pred_node.data
            return None

        # found node of with data equal to item
        if node.left is not None:
            # try to find the biggest node in the left subtree
            node = node.left
            while node.right is not None:
                node = node.right
            if pred_node is None:
                pred_node = node
            elif node.data > pred_node.data:
                pred_node = node
        elif pred_node is None:
            return None

        return pred_node.data