import urllib2
from lxml import etree

class StyleNode:
    def __init__(self, elements, page_occurrences=1):
        # string value of all elements i.e. "table-img-table-"
        self.key = style_key_generator(elements)
        # list of node elements
        self.elements = elements
        # number of pages style node occurred
        self.occurr = page_occurrences
        print '(%s)-(%d)' % (self.key, self.occurr)

    def __str__(self):
        return self.key

    def __repr__(self):
        return self.key

    def __eq__(self, other):
        return self.key == other.key

    def increment(self):
        self.occurr += 1

    def overwrite_elements_with(self, element):

        stemp = []
        for e in element.iterchildren():
            content = None
            if len(e) == 0:
                content = e.text
                stemp.append(ElementNode(e.tag, e.attrib, [StyleNode([])], content=content).overwrite_children(e))
        self.elements = stemp
        self.key = style_key_generator(self.elements)


def style_key_generator(elements):
    key = ''
    for e in elements:
        key += (e.tag+'-')
    return key


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
    # make ElementNode iterable.
    def __getitem__(self, index):
        return self.children[index]

    def __len__(self):
        return len(self.children)

    def add_new_elements(self, other):
        for e1, e2 in zip(self, other):
            if e1 == e2:
                e1.increment()
                e1.add_new_elements(e2)
            else:
                self.children.append(e2)

    def overwrite_children(self, root):
        stemp = []
        for e in root.iterchildren():
            stemp.append(ElementNode(e.tag, e.attrib, [StyleNode([]).overwrite_elements_with(e)]))

        new_element = ElementNode(root.tag, root.attrib, [StyleNode(stemp)])
        new_style = StyleNode([new_element])
        self.children = [new_style]


class PageTree:
    def __init__(self, url):
        # downloading and converting to DOM tree
        page_string = urllib2.urlopen(url)
        parser = etree.HTMLParser(remove_comments=True)
        tree = etree.parse(page_string, parser)

        # setting tag: Body as root.
        for e in tree.iter():
            if e.tag == 'body':
                self.dom = e
                break

        # building
        self.root = ElementNode('root', {}, [StyleNode([])])
        self.root.overwrite_children(self.dom)


class StyleTree:
    def __init__(self):
        self.root = ElementNode('root', {}, [StyleNode([])])

    def add_page(self, page_tree):
        self.root.add_new_elements(page_tree.root)
