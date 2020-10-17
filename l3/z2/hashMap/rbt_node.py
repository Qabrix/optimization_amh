from .node import Node
from .consts import BLACK, RED, NIL


class RbtNode(Node):
    def __init__(self, val=0, color=RED, parent=None, left=None, right=None):
        self.color = color
        self.parent = parent
        super().__init__(left, right, val)

    def __iter__(self):
        if self.left.color != NIL:
            yield from self.left.__iter__()

        yield self.val

        if self.right.color != NIL:
            yield from self.right.__iter__()
