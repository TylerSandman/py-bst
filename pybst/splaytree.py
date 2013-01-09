#!/usr/bin/env python
# Author: Tyler Sanderson <tylerbtbam@gmail.com>
#
# This file is part of PyBST.
#
# PyBST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyBST.  If not, see <http://www.gnu.org/licenses/>.

import collections
import bstree

Node = bstree.Node
BSTree = bstree.BSTree

class SplayNode(Node):
    """Represents a node of a Splay Tree"""
    def __init__(self,key,value):
        """Initializes a BST Node to represent a Splay Node"""
        Node.__init__(self,key,value)

class SplayTree(BSTree):
    """
    SplayTree implements a self-adjusting AVL Tree.

    A Splay Tree is an ordered node based tree key structure
    in which each node has at most two children, and everytime a
    node is accessed via search, insertion, or deletion, it is splayed
    to the root of the tree.

    For more information regarding Splay Trees, see:
    http://en.wikipedia.org/wiki/Splay_Tree

    Constructors:

    SplayTree() -> Creates a new empty Splay Tree
    SplayTree(seq) -> Creates a new Splay Tree from the elements in sequence [(k1,v1),(k2,v2),...,(kn,vn)]

    For further explanation of some functions or their source code, see bstree.py.
    """
    def __init__(self,*args):
        """Initialzes tree the same as as BST"""
        BSTree.__init__(self,*args)

    def is_valid(self, *args):
        """
        T.is_valid(...) -> Boolean. Produces True if and only if
        T is a valid Splay Tree. Note a valid Splay Tree has the exact same properties
        as a valid BST. Raises an exception otherwise.
        """
        if len(args) == 0:
            node = self.Root
        else:
            node = args[0]

        if not node:
            return True

        if node.left:
            if not node.left.parent == node:
                raise Exception("Left child of node " + str(node.key) + " is adopted by another node!")

        if node.right:
            if not node.right.parent == node:
                raise Exception("Right child of node " + str(node.key) + " is adopted by another node!")

        if node.parent and node.parent.left == node:
            if node.key > node.parent.key:
                raise Exception("Node " + str(node.key) + " is to the left of " + str(node.parent.key) + " but is larger")

        if node.parent and node.parent.right == node:
            if node.key < node.parent.key:
                raise Exception("Node " + str(node.key) + " is to the right of " + str(node.parent.key) + " but is smaller")

        return (self.is_valid(node.left) and self.is_valid(node.right))

    def preorder(self,*args):
        """
        T.preorder(...) -> Sequence. Produces a sequence of the Nodes
        in T, obtained in preorder.
        """
        return BSTree.preorder(self,*args)

    def inorder(self,*args):
        """
        T.inorder(...) -> Sequence. Produces a sequence of the Nodes
        in T, obtained in inorder.
        """
        return BSTree.inorder(self,*args)

    def postorder(self,*args):
        """
        T.postorder(...) -> Sequence. Produces a sequence of the Nodes
        in T, obtained in postorder.
        """
        return BSTree.postorder(self,*args)

    def levelorder(self):
        """
        T.levelorder(...) -> Sequence. Produces a sequence of the Nodes
        in T, obtained in levelorder.
        """
        return BSTree.levelorder(self,*args)

    def _get_node_without_splaying(self,key,*args):
        """
        T.get_node(key,...) -> Node. Produces the Node in T with key
        attribute key without rotating it to the root of T.
        If there is no such Node, produces None.
        """
        return BSTree.get_node(self,key,*args)

    def get_node(self,key,*args):
        """
        T.get_node(key,...) -> Node. Produces the Node in T with key
        attribute key and _rotates it to the root of T.
        If there is no such Node, produces None.
        """
        if len(args) == 0:
            start = self.Root
        else:
            start = args[0]
        if not start:
            return None
        if key == start.key:
            self._rotate_to_root(start)
            return start
        elif key > start.key:
            return self.get_node(key,start.right)
        else:
            return self.get_node(key,start.left)

    def insert(self,key,value,*args):
        """
        T.insert(key,value...) <==> T[key] = value. Inserts
        a new Node with key attribute key and value attribute
        value into T and _rotates it to the root of T.
        """
        if not isinstance(key,(int,long,float)):
            raise TypeError(str(key) + " is not a number")
        else:
            if not self.Root:
                self.Root = Node(key,value)
            elif len(args) == 0:
                if not self._get_node_without_splaying(key, self.Root):
                    self.insert(key,value,self.Root)
            else:
                child = Node(key,value)
                parent = args[0]
                if child.key > parent.key:
                    if not parent.right:
                        parent.right = child
                        child.parent = parent
                        self._rotate_to_root(child)
                    else:
                        self.insert(key,value,parent.right)
                else:
                    if not parent.left:
                        parent.left = child
                        child.parent = parent
                        self._rotate_to_root(child)
                    else:
                        self.insert(key,value,parent.left)

    def insert_from(self,seq):
        """
        T.insert_from(seq). For every key, value pair in seq,
        inserts a new Node into T with key and value attributes
        as given.
        """
        BSTree.insert_from(self,seq)

    def get_max(self,*args):
        """
        T.get_max(...) -> Node. Produces the Node that has the maximum
        key attribute in T.
        """
        return BSTree.get_max(self,*args)

    def get_min(self,*args):
        """
        T.get_min(...) -> Node. Produces the Node that has the minimum
        key attribute in T.
        """
        return BSTree.get_min(self,*args)

    def get_element_count(self,*args):
        """
        T.get_element_count(...) -> Nat. Produces the number of elements
        in T.
        """
        return BSTree.get_element_count(self,*args)

    def get_height(self,*args):
        """
        T.get_height(...) -> Nat. Produces the height of T, defined
        as one added to the height of the tallest subtree.
        """
        return BSTree.get_height(self,*args)

    def _rotate_left(self,pivot):
        """
        T.__rotate_left(pivot). Performs a left tree rotation in T
        around the Node pivot.
        """
        old_root = pivot
        par_node = old_root.parent

        new_root = old_root.right
        temp = new_root.right
        old_root.right = new_root.left

        if (old_root.right):
            old_root.right.parent = old_root
        new_root.left = old_root
        old_root.parent = new_root

        if par_node is None:
            self.Root = new_root
            self.Root.parent = None
        else:
            if par_node.right and par_node.right.key == old_root.key:
                par_node.right = new_root
                new_root.parent = par_node
            elif par_node.left and par_node.left.key == old_root.key:
                par_node.left = new_root
                new_root.parent = par_node

    def _rotate_right(self,pivot):
        """
        T.__rotate_right(pivot). Performs a right tree rotation in T
        around the Node pivot.
        """
        old_root = pivot
        par_node = old_root.parent

        new_root = old_root.left
        temp = new_root.left
        old_root.left = new_root.right

        if (old_root.left):
            old_root.left.parent = old_root

        new_root.right = old_root
        old_root.parent = new_root

        if par_node is None:
            self.Root = new_root
            self.Root.parent = None
        else:
            if par_node.right and par_node.right.key == old_root.key:
                par_node.right = new_root
                new_root.parent = par_node
            elif par_node.left and par_node.left.key == old_root.key:
                par_node.left = new_root
                new_root.parent = par_node

    def _rotate_to_root(self,node):
        """
        T._rotate_to_root(node). Uses appropriate tree rotations
        to _rotate (splay) node to the root of T.
        """
        parent = node.parent

        if parent:

            grandparent = parent.parent
            if not grandparent:
                if parent.left == node:
                    self._rotate_right(parent)
                else:
                    self._rotate_left(parent)

            elif grandparent.left == parent and parent.left == node:
                self._rotate_right(grandparent)
                self._rotate_right(parent)

            elif grandparent.right == parent and parent.right == node:
                self._rotate_left(grandparent)
                self._rotate_left(parent)

            elif grandparent.left == parent and parent.right == node:
                self._rotate_left(parent)
                self._rotate_right(grandparent)

            elif grandparent.right == parent and parent.left == node:
                self._rotate_right(parent)
                self._rotate_left(grandparent)

            self._rotate_to_root(node)

    def _delete_leaf(self,node):
        """
        T.__delete_leaf_parent(node). Deletes node from T, treating it
        as a Node with only one child.
        """
        par_node = node.parent

        if par_node:
            if par_node.left == node:
                par_node.left = None
            else:
                par_node.right = None

            del node

        else:
            self.Root = None

    def _delete_leaf_parent(self,node):
        """
        T.__delete_leaf_parent(node). Deletes node from T, treating it
        as a Node with only one child.
        """
        par_node = node.parent

        if node.key == self.Root.key:
            if node.right:
                self.Root = node.right
                node.right = None
            else:
                self.Root = node.left
                node.left = None

        else:
            if par_node.right == node:
                if node.right:
                    par_node.right = node.right
                    par_node.right.parent = par_node
                    node.right = None
                else:
                    par_node.right = node.left
                    par_node.right.parent = par_node
                    node.left = None
            else:

                if node.right:
                    par_node.left = node.right
                    par_node.left.parent = par_node
                    node.right = None
                else:
                    par_node.left = node.left
                    par_node.left.parent = par_node
                    node.left = None

        del node

    def _switch_nodes(self,node1,node2):
        """
        T.__switch_nodes(node1,node2). Switches positions
        of node1 and node2 in T.
        """
        BSTree._switch_nodes(self,node1,node2)

    def _delete_node(self,node):
        """
        T.__delete_node(node). Deletes node from T, treating it as
        a Node with two children.
        """
        if self.get_height(node.left) > self.get_height(node.right):
            to_switch = self.get_max(node.left)
            self._switch_nodes(node,to_switch)

            if not (to_switch.right or to_switch.left):
                to_delete = self.get_max(node.left)
                self._delete_leaf(to_delete)
            else:
                to_delete = self.get_max(node.left)
                self._delete_leaf_parent(to_delete)
        else:
            to_switch = self.get_min(node.right)
            self._switch_nodes(node,to_switch)

            if not (to_switch.right or to_switch.left):
                to_delete = self.get_min(node.right)
                self._delete_leaf(to_delete)
            else:
                to_delete = self.get_min(node.right)
                self._delete_leaf_parent(to_delete)

    def delete(self,key):
        """T.delete(key) <==> del T[key]. Deletes the Node
        with key attribute key from T.
        """
        node = self._get_node_without_splaying(key,self.Root)
        parent = node.parent

        if node:
            if not (node.left or node.right):
                self._delete_leaf(node)

            elif not (node.left and node.right):
                self._delete_leaf_parent(node)

            else:
                self._delete_node(node)

            if parent:
                self._rotate_to_root(parent)

    def delete_from(self,seq):
        """
        T.delete_from(seq). For every keyin seq, deletes
        the Node with that key attribute from T.
        """
        if isinstance(seq,collections.Iterable):
            for x in seq:
                self.delete(x)
        else:
            raise TypeError(str(iter) + " is not iterable")