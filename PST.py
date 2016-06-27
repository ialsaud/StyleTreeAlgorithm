from Node import Node
import urllib2
from lxml import html


class PST():
    """
    # This module contains the building blocks of the page Style Tree.
    """
    def __init__(self, url):
        page_string = urllib2.urlopen(url)
        root = html.fromstring(page_string.read())
        self.root = self.build(root)

    """
    builds the PST recursively
    """
    def build(self, root):
        children = []
        for e in root:
            new_child = self.build(e)
            if self.is_comment(new_child) is False: ## add to children if it's not comment node only
                children.append(new_child)
        children_ = [1,children]

        if root.text is not None:
            root.text = root.text.encode('ascii', 'ignore').decode('ascii') ##some of the text provided mosut be encoded
        else: ## Replace the None content with empty string
            root.text = ''

        return Node(root.tag, root.attrib, children_, root.text)

    """
    checks whether the node is a comment
    """
    def is_comment(self, node):
        w = str(node.tag).split()
        if w[0] == "<cyfunction":
            return True
        else:
            return False


########## SST stuf ############
def increment(children_set):
    children_set[0] += 1

"""
def BuildSST(SST, root2): ## this should be an SST with a PST

    if SST.children == None:


    if root1.children[1] == root2.children[1]:
        root1.children = [[1]]
    elif root1.children != root2.children:
        root1.children.append(root2.children) ## does this make a copy of children_set2
    for child1, child2 in zip(root1.children[1], root1.children[1]): ##loops in parallel
        comparator(child1, child2)
"""







########## TEST ############
x = PST('http://www.securityfocus.com/bid/83265')
x2 = PST('http://www.securityfocus.com/bid/83265')
y = PST('https://3.basecamp.com/3273604/projects/481759')
z = PST('http://www.securityfocus.com/bid/69077')

print x.root
SST = Node(x.root.tag, x.root.tag, None, x.root.text) ## empty node with the same information as one of the roots (all roots all the same)
print x.node






########## Scratch ##########

"""
        print (x.root)

        comparator(x.root,y.root)

        print x.root

"""

"""
        from lxml import html
        import urllib2

        A = urllib2.urlopen("url")
        root = html.from_string(A.read())
        root.text_content #prints the whole pag
"""

"""
        import inspect
        print inspect.getargspec(fromstring)
        shows the arguments of a method

        dir(fromstring)
        shows the methods
"""