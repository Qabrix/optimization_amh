import sys
from .rbt_node import RbtNode
from .structure import Structure
from .consts import BLACK, RED, NIL

class RbtStructure(Structure):
    def __init__(self):
        self.NIL_LEAF = RbtNode(0, NIL)
        self.root = self.NIL_LEAF
        super().__init__(self.root)

    def insert(self, key):
        self.count += 1
        key = self.prepare_word(key)
        node = RbtNode(key)
        node.parent = None
        node.val = key
        node.left = self.NIL_LEAF
        node.right = self.NIL_LEAF
        node.color = RED 

        y = None
        x = self.root

        while x != self.NIL_LEAF:
            y = x
            if node.val < x.val:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.val < y.val:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = BLACK
            return

        if node.parent.parent == None:
            return

        self.__fix_insert(node)

    def min(self): 
        if self.root:
            return self.min_node(self.root)
        else:
            return None
    
    def min_node(self, node):
        current = node 
        while current != self.NIL_LEAF: 
            if current.left == self.NIL_LEAF: 
                break
            current = current.left 
    
        return current 

    def max(self): 
        if self.root:
            return self.max_node(self.root)
        else:
            return None
    
    def max_node(self, node):
        current = node 
        while current != self.NIL_LEAF: 
            if current.right == self.NIL_LEAF: 
                break
            current = current.right 
    
        return current 

    def __in_order_helper(self, node):
        if node != self.NIL_LEAF:
            self.__in_order_helper(node.left)
            sys.stdout.write(node.val + " ")
            self.__in_order_helper(node.right)

    def __search_tree_helper(self, node, key):
        if node == self.NIL_LEAF or key == node.val:
            return node

        self.find_counter += 1
        if key < node.val:
            return self.__search_tree_helper(node.left, key)
        return self.__search_tree_helper(node.right, key)

    def __iter__(self):
        if not self.root:
            return list()
        yield from self.root.__iter__()

    def __fix_delete(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == RED:
                    s.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == BLACK and s.right.color == BLACK:
                    s.color = RED
                    x = x.parent
                else:
                    if s.right.color == BLACK:
                        s.left.color = BLACK
                        s.color = RED
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = BLACK
                    s.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == RED:
                    s.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == BLACK and s.right.color == BLACK:
                    s.color = RED
                    x = x.parent
                else:
                    if s.left.color == BLACK:
                        s.right.color = BLACK
                        s.color = RED
                        self.left_rotate(s)
                        s = x.parent.left 

                    s.color = x.parent.color
                    x.parent.color = BLACK
                    s.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, val):
        return self.__delete_node_helper(self.root, val)

    def __delete_node_helper(self, node, key):
        z = self.NIL_LEAF
        while node != self.NIL_LEAF:
            if node.val == key:
                z = node

            if key < node.val:
                node = node.left
            else:
                node = node.right

        if z == self.NIL_LEAF:
            return 0

        self.count -= 1
        y = z
        y_original_color = y.color
        if z.left == self.NIL_LEAF:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.NIL_LEAF):
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.min_node(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.__fix_delete(x)
        
        return 1
    
    def  __fix_insert(self, k):
        while k.parent.color == RED:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left 
                if u.color == RED:
                    u.color = BLACK
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)

                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right 

                if u.color == RED:
                    u.color = BLACK
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    k = k.parent.parent 
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)

                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = BLACK

    def inorder(self):
        self.__in_order_helper(self.root)

    def find(self, key):
        self.reset_find_counter()
        return self.__search_tree_helper(self.root, key)

    def successor(self, key):
        node = self.find(key)

        def successor_node(node):
            if node.right is not None and node.right.color != NIL: 
                return self.min_node(node.right) 

            succ = None
            root = self.root

            while root:
                if node.color == NIL:
                    break

                if node.val < root.val:
                    succ = root
                    root = root.left
                elif node.val > root.val:
                    root = root.right
                else:
                    break

            return succ
        if node:
            return successor_node(node)
        else:
            return None
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL_LEAF:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL_LEAF:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y