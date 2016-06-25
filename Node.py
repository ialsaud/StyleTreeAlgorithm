
class Node():
    def __init__(self, tag, attrs, children):
        self.tag = tag
        self.attrs = attrs
        self.children = children

    def __repr__(self, level=0):
        ret = ("\t"*level) +  self.print_node() + "\n"
        for child in list(self.children[1]):
            ret += child.__repr__(level+1)
        return ret

    def __cmp__(self, other):
        assert Ture

    def print_node(self):
        return "(%s)" % (self.tag)