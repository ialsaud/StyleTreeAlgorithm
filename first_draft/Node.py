
class Node:

    """
    initializes the node with the required data
    """
    def __init__(self, tag, attrib, children, content):
        self.tag = tag
        self.attrib = attrib
        self.content = content
        self.children = children #array of nodes
    """
    prints the tree with indentations to indicate depth or level
    """
    def __repr__(self, level=0):
        ret = ("\t"*level) + self.print_node() + "\n"
        for child in self.children[0][1]: ## for PST self.children
            ret += child.__repr__(level+1)
        return ret

    """
    overrides the '==' function.
    note: that this will go over the children and will check their equality to each other.
    """
    def __eq__(self, other):
        if self.tag != other.tag:
            return False
        if not (compare_dictionaries(self.attrib, other.attrib)):
            return False
        """
        for child1, child2 in zip(self.children[1], other.children[1]):
            if child1.__ne__(child2):  ## TODO should we go all the way down the tree
                return False
        """
        return True
    """
    not equal method
    """
    def __ne__(self, other):
        return self.__eq__(other)

    """
    this methods can be modified to print node data (tag, attributes, or children set)
    """
    def print_node(self):
        children =[]
        for child in self.children[0][1]: ## for PST self.children
            children.append(child.tag)
        count = self.children[0][0] # for PST no count
        return "(%s, %s, %d)" % (self.tag, children, count)

    """
    this method compares the node attribute dictionaries
    """
def compare_dictionaries(dict1, dict2):
    for key in set(dict1.keys()).union(dict2.keys()):
        if key not in dict1:
            return False
        elif key not in dict2:
            return False
        elif dict1[key] != dict2[key]:
            return False
    return True
