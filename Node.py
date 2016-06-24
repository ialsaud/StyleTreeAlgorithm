
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

    def print_node(self):
        l = []
        for child in list(self.children[1]):
            l.append(child.tag)
        return "(%s)" % (self.tag)