from Node import Node
import urllib2
from lxml.html import fromstring


# This module contains the building blocks of the page Style Tree.
class PST():
    def __init__(self, url):
        page_string = urllib2.urlopen(url)
        root = fromstring(page_string.read())
        self.root = root
        self.node = self.build(root)


    def build(self, root):
        children = set()
        for e in root:
            new_child = self.build(e)
            children.add(new_child)
        children = (1,children)
        return Node(root.tag, root.attrib, children)

x = PST('http://www.securityfocus.com/bid/83265')

print x.node














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