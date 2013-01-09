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

class RBNode(Node):
    """Represents a node of a balanced Red Black Tree"""
    def __init__(self,key,value):
        """Initializes a BST node, then add color attribute"""
        Node.__init__(self,key,value)
        self.color = 'r'

class RBTree(BSTree):
    """
    AVLTree implements a self-balancing Red Black Tree.

    An AVL Tree is an ordered node based tree key structure
    in which each node has at most two children, and follows these rules:
    1. A node is either red or black.
    2. The root is black. (This rule is sometimes omitted)
    3. All null children (children of leaves) are black.
    4. Both children of every red node are black.
    5. Every simple path from a given node to any of its descendant leaves
    contains the same number of black nodes.

    For more information regarding Red Black Trees, see:
    http://en.wikipedia.org/wiki/Red_black_tree

    Constructors:

    RBTree() -> Creates a new empty Red Black tree
    RBTree(seq) -> Creates a new Red Black Tree from the elements in sequence [(k1,v1),(k2,v2),...,(kn,vn)]

    For further explanation of some functions or their source code, see bstree.py.
    """
    def __init__(self,*args):
        """Initializes tree the same as a BST"""
        BSTree.__init__(self,*args)

    def _get_all_leaf_paths(self):
        """
        T._get_all_leaf_paths() -> Sequence. Produces a sequence
        of all simple paths from all nodes to leaves in T.
        """
        all_leafpaths = []
        nodelist = self.preorder()
        for node in nodelist:
            all_leafpaths.append(self._get_all_leaf_paths_from(node))
        return all_leafpaths

    def _get_all_leaf_paths_from(self,node, acc=[]):
        """
        T._get_all_leaf_paths_from(node,acc) -> Sequence. Produes
        a sequence of all simple paths from all nodes to leaves
        in T starting from the Node node.
        """
        leafpaths = []

        if not node.left and not node.right:
            leafpaths.append([node]+acc)

        if node.left:
            for leaf_path in self._get_all_leaf_paths_from(node.left, [node]+acc):
                leafpaths.append(leaf_path)
        if node.right:
            for leaf_path in self._get_all_leaf_paths_from(node.right, [node]+acc):
                leafpaths.append(leaf_path)

        return leafpaths

    def is_valid(self,*args):
        """
        T.is_valid(...) -> Boolean. Produces True if and only if
        T is a valid Red Black Tree. Raises an exception otherwise.
        """
        if len(args) == 0:
            node = self.Root
            all_leafpaths = self._get_all_leaf_paths()
            for leafpaths in all_leafpaths:
                black_count_list = []
                for path in leafpaths:
                    black_count = 0
                    for node in path:
                        if node.color == 'k':
                            black_count = black_count + 1
                    black_count_list.append(black_count)

                if not black_count_list[1:] == black_count_list[:-1]:
                    raise Exception("Not all simple paths in  " + str(self) + " have same amount of black nodes!")

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

        if node.color == 'r':
            if ((node.left and node.left.color == 'r') or
                (node.right and node.right.color == 'r')):
                    raise Exception("Node " + str(node.key) + " is red and has a red child!")

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

    def get_node(self,key,*args):
        """
        T.get_node(key,...) -> Node. Produces the node in T with key
        attribute key. If there is no such node, produces None.
        """
        return BSTree.get_node(self,key,*args)

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
        if not pivot.left:
            pass

        else:

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

    def _insert_case_one(self,child):
        """
        T._insert_case_one(child). Considers the case in which
        child is at the root of the tree. Recolors black if so,
        otherwise moves on to case two.
        """
        node = child
        par_node = node.parent

        if not par_node:
            self.Root.color = 'k'
        else:
            self._insert_case_two(node)

    def _insert_case_two(self,child):
        """
        T._insert_case_two(child). Considers the case in which
        child's parent is black. If so, we are done. If not, moves
        to case three.
        """
        node = child
        par_node = node.parent

        if par_node.color == 'r':
            self._insert_case_three(node)

    def _insert_case_three(self,child):
        """
        T._insert_case_three(child). Considers the case in which
        child's parent and uncle are red. If so, recolors
        the parent and uncle black, and child's grandparent red.
        Note child's grandparent now may have a red parent, which
        makes T invalid. So now we start over from case one at
        the grandparent.
        """
        node = child
        par_node = node.parent
        grand_node = par_node.parent
        if grand_node.left == par_node:
            uncle = grand_node.right
        else:
            uncle = grand_node.left

        if uncle and uncle.color == 'r':
            grand_node.color = 'r'
            par_node.color = 'k'
            uncle.color = 'k'
            self._insert_case_one(grand_node)
        else:
            self._insert_case_four(node)

    def _insert_case_four(self,child):
        """
        T._insert_case_four(child). Considers the case in which
        child's parent is red, child's uncle is black, and
        the parent is the left child of the grandparent while
        the child is the right child of the parent, or vice versa.
        If so, performs an appropriate tree rotation around
        child's parent and moves on to case five.
        """
        node = child
        par_node = node.parent
        grand_node = par_node.parent
        if grand_node.left == par_node:
            uncle = grand_node.right
        else:
            uncle = grand_node.left

        if grand_node.left == par_node and par_node.right == node:
                self._rotate_left(par_node)
                node = node.left
        elif grand_node.right == par_node and par_node.left == node:
                self._rotate_right(par_node)
                node = node.right

        self._insert_case_five(node)

    def _insert_case_five(self,child):
        """
        T._insert_case_five(child). Considers the case in which
        child's parent is red, child's uncle is black, and the
        parent is the left child of the grandparent while the child
        is the left child of the parent, or vice versa. If so,
        performs an appropriate tree rotation around the grandparent.
        """
        node = child
        par_node = node.parent
        grand_node = par_node.parent
        if grand_node.left == par_node:
            uncle = grand_node.right
        else:
            uncle = grand_node.left

        if par_node.left == node:
                grand_node.color = 'r'
                par_node.color = 'k'
                self._rotate_right(grand_node)
        elif par_node.right == node:
                grand_node.color = 'r'
                par_node.color = 'k'
                self._rotate_left(grand_node)

    def insert(self,key,value,*args):
        """
        T.insert(key,value...) <==> T[key] = value. Inserts
        a new Node with key attribute key and value attribute
        value into T. Recolours T and performs tree rotations as necessary.
        Note: For more information on the cases to be considered for insertion,
        see: http://en.wikipedia.org/wiki/Red-black_tree
        """
        if not isinstance(key,(int,long,float)):
            raise TypeError(str(key) + " is not a number")
        else:
            if not self.Root:
                self.Root = RBNode(key,value)
                self.Root.color = 'k'
            elif len(args) == 0:
                if not self.get_node(key,self.Root):
                        self.insert(key,value,self.Root)

            else:
                child = RBNode(key,value)
                parent = args[0]
                if child.key > parent.key:
                    if not parent.right:
                        parent.right = child
                        child.parent = parent
                        if parent.color == 'r':
                            self._insert_case_one(child)
                    else:
                        self.insert(key,value,parent.right)
                else:
                    if not parent.left:
                        parent.left = child
                        child.parent = parent
                        if parent.color == 'r':
                            self._insert_case_one(child)
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

    def _delete_case_one(self,child,parent):
        """
        T._delete_case_one(child,parent). Considers the case in which
        child is the new root. If so, we are done. If not, move on to
        case two.
        """
        if parent:
            self._delete_case_two(child,parent)

    def _delete_case_two(self,child,parent):
        """
        T._delete_case_two(child,parent). Considers the case in which
        child's sibling is red. If so, reverse the colors of parent
        and sibling, and perform an appropriate tree rotation
        around the parent. Move on to case three.
        """
        node = child
        par_node = parent

        if par_node.left == node:
            sib_node = par_node.right
        elif par_node.right == node:
            sib_node = par_node.left

        if sib_node and sib_node.color == 'r':
            sib_node.color = 'k'
            par_node.color = 'r'
            if par_node.left == node:
                self._rotate_left(par_node)
            else:
                self._rotate_right(par_node)

        self._delete_case_three(node,par_node)

    def _delete_case_three(self,child,parent):
        """
        T._delete_case_three(child,parent). Considers the case in which
        parent, child's sibling, and the sibling's children are all
        black. If so, recolor child's sibling red and start over
        from case one from parent. If not, move on to case four.
        """
        node = child
        par_node = parent

        if par_node.left == node:
            sib_node = par_node.right
        elif par_node.right == node:
            sib_node = par_node.left

        if ((sib_node and sib_node.color == 'k') or (not sib_node)):
            sib_color = 'k'
        else:
            sib_color = 'r'

        if ((sib_node and sib_node.left and sib_node.left.color == 'k') or (not sib_node or not sib_node.left)):
            sib_left_color = 'k'
        else:
            sib_left_color = 'r'

        if ((sib_node and sib_node.right and sib_node.right.color == 'k') or (not sib_node or not sib_node.right)):
            sib_right_color = 'k'
        else:
            sib_right_color = 'r'

        if par_node.color == 'k' and sib_color == 'k' and sib_left_color == 'k' and sib_right_color == 'k':
            sib_node.color = 'r'
            self._delete_case_one(par_node,par_node.parent if par_node.parent else None)
        else:
            self._delete_case_four(node,par_node)

    def _delete_case_four(self,child,parent):
        """
        T._delete_case_four(child,parent). Considers the case in which
        child's sibling and its children are black, but parent is red.
        If so, we swap the colors of the sibling and parent.
        If not, move on to case five.
        """
        node = child
        par_node = parent

        if par_node.left == node:
            sib_node = par_node.right
        elif par_node.right == node:
            sib_node = par_node.left

        if ((sib_node and sib_node.color == 'k') or (not sib_node)):
            sib_color = 'k'
        else:
            sib_color = 'r'

        if ((sib_node and sib_node.left and sib_node.left.color == 'k') or (not sib_node or not sib_node.left)):
            sib_left_color = 'k'
        else:
            sib_left_color = 'r'

        if ((sib_node and sib_node.right and sib_node.right.color == 'k') or (not sib_node or not sib_node.right)):
            sib_right_color = 'k'
        else:
            sib_right_color = 'r'

        if par_node.color == 'r' and sib_color == 'k' and sib_left_color == 'k' and sib_right_color == 'k':
            sib_node.color = 'r'
            par_node.color = 'k'
        else:
            self._delete_case_five(node,par_node)

    def _delete_case_five(self,child,parent):
        """
        T._delete_case_five(child,parent). Considers the case in which
        child's sibling is black, its left child is red, its right
        child is black, and child is the left child of parent.
        Also considers the mirror case to this. If so, perform
        an appropriate tree rotation around the sibling, and
        swap the colors of the sibling and its new parent.
        Move on to case six.
        """
        node = child
        par_node = parent

        if par_node.left == node:
            sib_node = par_node.right
        elif par_node.right == node:
            sib_node = par_node.left

        if ((sib_node and sib_node.color == 'k') or (not sib_node)):
            sib_color = 'k'
        else:
            sib_color = 'r'

        if ((sib_node and sib_node.left and sib_node.left.color == 'k') or (not sib_node or not sib_node.left)):
            sib_left_color = 'k'
        else:
            sib_left_color = 'r'

        if ((sib_node and sib_node.right and sib_node.right.color == 'k') or (not sib_node or not sib_node.right)):
            sib_right_color = 'k'
        else:
            sib_right_color = 'r'

        if sib_color == 'k':

            if par_node.left == node and sib_right_color == 'k' and sib_left_color == 'r':
                sib_node.color = 'r'
                sib_node.left.color = 'k'
                self._rotate_right(sib_node)
            elif par_node.right == node and sib_left_color == 'k' and sib_right_color == 'r':
                sib_node.color = 'r'
                sib_node.right.color = 'k'
                self._rotate_left(sib_node)

        self._delete_case_six(node,par_node)

    def _delete_case_six(self,child,parent):
        """
        Considers the case in which child's sibling is black,
        its right child is red, and child is the left child of parent.
        Also considers the mirror of this case. If so, perform
        an appropriate tree rotation around parent, so that child's sibling
        becomes the parent of parent and the sibling's right child.
        Then exchange the colors of parent and child's sibling, and
        make the sibling's red child black. We are done.
        """
        node = child
        par_node = parent

        if par_node.left == node:
            sib_node = par_node.right
        elif par_node.right == node:
            sib_node = par_node.left

        if ((sib_node and sib_node.color == 'k') or (not sib_node)):
            sib_color = 'k'
        else:
            sib_color = 'r'

        if ((sib_node and sib_node.left and sib_node.left.color == 'k') or (not sib_node or not sib_node.left)):
            sib_left_color = 'k'
        else:
            sib_left_color = 'r'

        if ((sib_node and sib_node.right and sib_node.right.color == 'k') or (not sib_node or not sib_node.right)):
            sib_right_color = 'k'
        else:
            sib_right_color = 'r'

        if par_node.left == node and sib_color == 'k' and sib_right_color == 'r':
            sib_node.color = par_node.color
            par_node.color = 'k'
            sib_node.right.color = 'k'
            self._rotate_left(par_node)
        elif par_node.right == node and sib_color == 'k' and sib_left_color == 'r':
            sib_node.color = par_node.color
            par_node.color = 'k'
            sib_node.left.color = 'k'
            self._rotate_right(par_node)

    def _delete_leaf(self,node):
        """
        T.__delete_leaf_parent(node). Deletes node from T, treating it
        as a Node with only one child.
        """
        par_node = node.parent
        node_color = node.color

        if par_node:
            if par_node.left == node:
                par_node.left = None
                new_node = None
            else:
                par_node.right = None
                new_node = None

            del node

        new_parent = par_node

        if node_color == 'k':
            self._delete_case_one(new_node,new_parent)

    def _delete_leaf_parent(self,node):
        """
        T.__delete_leaf_parent(node). Deletes node from T, treating it
        as a Node with only one child.
        """
        par_node = node.parent
        node_color = node.color
        if node.left:
            child_color = node.left.color
        else:
            child_color = node.right.color

        if node.key == self.Root.key:
            if node.right:
                self.Root = node.right
                self.Root.color = 'k'
                node.right = None
                new_node = node.right
            else:
                self.Root = node.left
                self.Root.color = 'k'
                node.left = None
                new_node= node.left

        else:
            if par_node.right == node:
                if node.right:
                    par_node.right = node.right
                    par_node.right.parent = par_node
                    node.right = None
                    if node_color == 'k' and child_color == 'r':
                        par_node.right.color = 'k'

                else:
                    par_node.right = node.left
                    par_node.right.parent = par_node
                    node.left = None
                    if node_color == 'k' and child_color == 'r':
                        par_node.right.color = 'k'

                new_node = par_node.right

            else:

                if node.right:
                    par_node.left = node.right
                    par_node.left.parent = par_node
                    node.right = None
                    if node_color == 'k' and child_color == 'r':
                        par_node.left.color = 'k'
                else:
                    par_node.left = node.left
                    par_node.left.parent = par_node
                    node.left = None
                    if node_color == 'k' and child_color == 'r':
                        par_node.left.color = 'k'

                new_node = par_node.left

        del node

        if node_color == 'k' and child_color == 'k':

            self._delete_case_one(new_node,par_node)

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
        BSTree._delete_node(self,node)

    def delete(self,key):
        """T.delete(key) <==> del T[key]. Deletes the Node
        with key attribute key from T. Recolours T and
        performs tree rotations as necessary. Note, for
        more information regarding the cases to be considered
        for deletion, see: http://en.wikipedia.org/wiki/Red-black_tree
        """
        node = self.get_node(key,self.Root)

        if node:
            if not (node.left or node.right):
                if node.parent:
                    self._delete_leaf(node)

            elif not (node.left and node.right):
                self._delete_leaf_parent(node)

            else:
                self._delete_node(node)

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