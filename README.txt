About
-----

PyBST implements Binary Trees, AVL Trees, Splay Trees, and Red Black Trees in Python. Furthermore, PyBST provides a module for plotting these trees using networkx and matplotlib.

Tree Classes Provided:

* BSTree - represents an unbalanced Binary Search Tree
* AVLTree - represents a balanced AVL Tree
* SplayTree - represents an adjusted Splay Tree
* RBTree - represents a balanced Red Black Tree

Constructor
-----------

Let Tree represent one of the provided tree classes mentioned above.

* Tree() - > Creates a new empty tree
* Tree(seq) -> Creates a new empty tree from seq [(key1,val1),(key2,val2),...,(keyn,valn)]

Methods
-------

Tree Methods:

* is_valid() -> Produces True if Tree is a valid tree of its type, else False.
* preorder() -> Produces a sequence of the Nodes in Tree in preorder.
* inorder() -> Produces a sequence of the Nodes in Tree in inorder.
* postorder() -> Produces a sequence of the Nodes in Tree in postorder.
* levelorder() -> Produces a sequence of the Nodes in Tree in levelorder.
* get_node(key) -> Produces the Node in Tree with key attribute key.
* insert(key,val) <==> Tree[key] = value. Inserts a new Node with key attribute key and value attribute val into Tree.
* insert_from(seq) -> Inserts keys and values from seq [(key1,val1),(key2,val2),...,(keyn,valn)] into Tree.
* get_max() <==> max(Tree). Produces the Node with the maximum key in Tree.
* get_min() <==> min(Tree). Produces the Node with the minimum key in Tree.
* get_element_count <==> len(Tree). Produces the number of elements in Tree.
* get_height() -> Produces the height of Tree.
* delete(key) <==> del Tree[key]. Deletes the Node with key attribute key from Tree.
* delete_from(seq) -> Deletes Nodes with keys from seq [key1,key2,...,keyn] from Tree.

Plotting Methods (draw Module):

* plot_tree(Tree) -> Provides a visual representation of Tree via plotting it using networkx and matplotlib.

Dependencies
------------

PyBST requires no external dependencies for the tree classes and their methods themselves. However, note that the following packages are required for tree plotting:

Networkx: http://networkx.github.com/

Matplotlib: http://matplotlib.org/

Installation
------------

From source::

    python setup.py install

Using easy install::

    easy_install pybst

Alternatively download one of the build distributions found under Downloads.

Download
--------
https://github.com/TylerSandman/PyBST/tree/master/dist

Documentation
-------------
See PyBST's github repository at: https://github.com/TylerSandman/PyBST/