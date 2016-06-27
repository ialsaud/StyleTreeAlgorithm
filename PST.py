from Node import Node
import urllib2
from lxml import html


# This module contains the building blocks of the page Style Tree.
class PST():
    def __init__(self, url):
        page_string = urllib2.urlopen(url)
        root = html.fromstring(page_string.read()) # this is uniform
        self.root = self.build(root)

    def build(self, root): # TODO we need to make this uniform\\ all good
        children = []
        for e in root:
            new_child = self.build(e)
            children.append(new_child)
        children_ = [1,children]
        return Node(root.tag, root.attrib, children_)


def increment(children_set):
    children_set[0] += 1


def comparator(root1, root2):
    if root1.children == root2.children_set2: ## TODO change compare method
        increment(root1.children)
    elif root1.children != root2.children:
        root1.children = [root1.children, root2.children] ## does this make a copy of children_set2

    for child1, child2 in zip(root1.children[1], root1.children[1]): ##loops in parallel
        comparator(child1, child2)


x = PST('http://www.securityfocus.com/bid/83265')
x2 = PST('http://www.securityfocus.com/bid/83265')
y = PST('http://www.securityfocus.com/bid/77216')
z = PST('http://www.securityfocus.com/bid/69077')

print x.root == y.root ## yeap it works.




# print (x.root)
#
# comparator(x.root,y.root)
#
#
# print x.root






# ==== Scratch =====

"""
        #SKRATCH
        #from lxml import html
        #import urllib2

        #A = urllib2.urlopen("url")
        #root = html.from_string(A.read())
        #root.text_content #prints the whole pag
"""

"""
        import inspect
        print inspect.getargspec(fromstring)
        shows the arguments of a method
        """

"""
        dir(fromstring)
        shows the methods
"""