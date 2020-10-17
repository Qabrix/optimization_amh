class Node:
    def __init__(self, left=None, right=None, val=None):
        self.left = left
        self.right = right
        self.val = val

    def has_children(self):
        return bool(self.get_children_count())

    def get_children_count(self):
        return sum([int(self.left != None), int(self.right != None)])
