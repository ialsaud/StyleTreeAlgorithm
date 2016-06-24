

class Node():
    def __init__(self, tag, attrs, children):
        self.tag = tag
        self.attrs = attrs
        self.children = children

    def __repr__(self):
        return "(Node with %s, {%s}, %s)" (self.tag)