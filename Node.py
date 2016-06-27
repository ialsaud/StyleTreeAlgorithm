
class Node:
    def __init__(self, tag, attrs, children):
        self.tag = tag
        self.attrs = attrs
        self.children = children

    def __repr__(self, level=0):
        ret = ("\t"*level) + self.print_node() + "\n"
        for child in list(self.children[1]):
            ret += child.__repr__(level+1)
        return ret

    # overrides the '==' function.
    # note that this will go over
    # the children and will check
    # their equality to each other.
    def __eq__(self, other):
        if self.tag != other.tag:
            return False
        if not (compare_dictionaries(self.attrs, other.attrs)):
            return False
        for child1, child2 in zip(self.children[1], other.children[1]):
            if child1.__ne__(child2):
                return False
        return True

    # not equal method
    def __ne__(self, other):
        return self.__eq__(other)

    def print_node(self):
        return "(%s)" % self.tag


def compare_dictionaries(dict1, dict2):
    for key in set(dict1.keys()).union(dict2.keys()):
        if key not in dict1:
            return False
        elif key not in dict2:
            return False
        elif dict1[key] != dict2[key]:
            return False
    return True
