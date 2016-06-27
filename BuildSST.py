from Node import Node
import urllib2
from lxml import html

class SST():
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
        children = [[1,children]]
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

