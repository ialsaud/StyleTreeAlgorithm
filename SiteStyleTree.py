import urllib2
from io import BytesIO
from lxml import etree


class StyleNode:
    def __init__(self, elements, page_occurrences=1):
        # string value of all elements i.e. "table-img-table-"
        self.key = style_key_generator(elements)
        # list of node elements
        self.elements = elements
        # number of pages style node occurred
        self.occur = page_occurrences

    def __str__(self):
        return self.key

    def __repr__(self):
        return self.key

    def __eq__(self, other):
        return self.key == other.key

    def __getitem__(self, index):
        return self.elements[index]

    def __len__(self):
        return len(self.elements)

    def increment(self):
        self.occur += 1


def style_key_generator(elements):
    key = ''
    for e in elements:
        key += (e.tag+'-')
    return key[0:-1]


class ElementNode:
    def __init__(self, tag, attrs, style_node, content=None):
        # string value
        self.tag = tag
        # dictionary of corresponding tag node attributes
        self.attrs = attrs
        # children represented in a list style node
        self.children = style_node
        # content shows whether node is leaf or not.
        self.content = content

    def __str__(self):
        return self.tag.__str__()

    def __repr__(self):
        return self.tag.__str__()

    def __eq__(self, other):
        return self.tag.__str__() == other.tag.__str__()

    # functions __getitem__ and __len__
    # make ElementNode iterable. TODO this is not necessary for now
    def __getitem__(self, index):
        return self.children[index]

    def __len__(self):
        return len(self.children)

    def add_new_elements(self, other):
        if len(self) == 0 or len(other) == 0:
            for s in other:
                self.children.append(s)
        else:
            for s1, s2 in zip(self, other):
                    if s1 == s2:    # table-
                        s1.increment()
                        for e1, e2 in zip(s1, s2):
                            e1.add_new_elements(e2)
                    else:
                        self.children.append(s2)


class PageTree:
    def __init__(self, url):
        # downloading and converting to DOM tree
        page_string = urllib2.urlopen(url)

        page_string = page_string.read()
        page_string = page_string.replace("</br>", "")
        page_string = page_string.replace("<br/>", "")
        page_string = page_string.replace("<br>", "")

        parser = etree.HTMLParser(remove_comments=True)
        tree = etree.parse(BytesIO(page_string), parser)  # DOM tree as etree

        for e in tree.getroot().iterchildren():
            if e.tag == 'body':
                body = e

        body_E = self.build_0(body)  # takes etree root (body) returns Element Node Body
        self.build_1(body_E)  # takes Element Node body, changes children to StyleNodes
        self.root = ElementNode('root', {}, [StyleNode([body_E])], None)

    def build_0(self, root): # takes e-tree node
        children = []

        for e in root.iterchildren():  # iterate etree object
            new_child = self.build_0(e)  # returns element nodes
            children.append(new_child)

        if len(root) == 0:
            if root.tag == 'img':
                return ElementNode(root.tag, root.attrib, children, root.attrib.get('src', None))
            return ElementNode(root.tag, root.attrib, children, root.text)
        return ElementNode(root.tag, root.attrib, children)

    def build_1(self, E):    # takes Element Node (root of SST/PST)
        E.children = [StyleNode(E.children)]
        for e in E.children[0].elements:
            self.build_1(e)


class StyleTree:
    def __init__(self):
        self.root = ElementNode('root', {}, [])

    def add_page(self, page_tree):
        self.root.add_new_elements(page_tree.root)
