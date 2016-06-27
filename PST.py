from Node import Node
import urllib2
from lxml import html
from BuildSST import SST
import BuildSST

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

        if root.text is not None:
            root.text = root.text.encode('ascii', 'ignore').decode('ascii') ##some of the text provided mosut be encoded
        else: ## Replace the None content with empty string
            root.text = ''

        return Node(root.tag, root.attrib, children, root.text)



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


"""
def BuildSST_(root, root1):

    root.children = [ [ 1,root1.children]  ]

    for child, child1 in zip(root.children[0][1], root1.children):
        BuildSST_(child,child1)
"""


def BuildSST(SS, root1): ## this should be an SST with a PST

    flag = 0
    for child_set in SS.children: #    [ [    ], [   ] , .... ] || child_set = [count, [set]]
        if child_set[1] == root1.children:
            flag = 1
            child_set[0] += 1
            for child, child_new in zip(child_set[1],root1.children):
                BuildSST(child,child_new)
            break

    if flag == 0:
        SS.children.append([1,root1.children])


########## TEST ############

x = PST('http://www.securityfocus.com/bid/83265')
x2 = PST('http://www.securityfocus.com/bid/83265')
y = PST('https://3.basecamp.com/3273604/projects/481759')
z = PST('http://www.securityfocus.com/bid/69077')


z = PST('http://www.securityfocus.com/bid/69077')
SS = SST('http://www.securityfocus.com/bid/83265')

#BuildSST_(SST.root, x.root)
BuildSST(SS.root, z.root)
BuildSST(SS.root, z.root)

print SS.root



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