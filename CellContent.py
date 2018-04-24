
class CellContent:
    def __init__(self,content,left,right):
        self.terminal = None
        if left == right:# they both None
            self.children = [None]
        else:
            self.children = [left,right]
        self.left_backpointer = left
        self.right_backpointer = right
        self.content = content