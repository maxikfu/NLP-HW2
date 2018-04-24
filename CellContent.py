
class CellContent:
    def __init__(self,content,left,right):
        self.terminal = None
        self.left_backpointer = left
        self.right_backpointer = right
        self.content = content