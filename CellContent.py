
class CellContent:
    def __init__(self,content,left,right):
        self.terminal = None
        if left == right:# they both None
            self.children = [None]
        else:
            self.children = [left,right]
        self.content = content
        self.parent = None