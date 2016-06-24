from Node import Node
import urllib2
from lxml import html

import json


# This module contains the building blocks of the page Style Tree.
class PST():
    def __init__(self, url):
        page_string = urllib2.urlopen(url)
        root = html.fromstring(page_string.read())
        self.node = self.build(root)

    def build(self, root):
        if root is not None:
            children = set()
            for e in root:
                new_child = self.build(e)
                if new_child is not None:
                    children.add(new_child)
            return Node(root.tag, root.attrib, children)
        return None

    def get_dict(self):
        return self.node.get_dict()

    def __repr__(self):
        return self.get_dict().__repr__()


def print_root(root):
    if root is not None:
        for e in root:
            print  e.tag
            print_root(e)


x = PST('http://www.securityfocus.com/bid/83265')

print json.dumps(x.get_dict(), indent=2)

#print_root(x.root)
#print x.root.text_content


#SKRATCH
#from lxml import html
#import urllib2

    #A = urllib2.urlopen("url")
    #root = html.from_string(A.read())
    #
    #root.text_content #prints the whole page!
