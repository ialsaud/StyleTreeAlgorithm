import urllib2
from io import BytesIO
from lxml import etree

class style_node:
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

class content_node:
    def __init__(self):
        self.count = 0 # counter for the different content it has
        self.repeat_list = []
        self.content_list = []

    def add_content(self, content):
        flag = False
        i = 0
        for c in self.content_list:
            if c == content:
                self.repeat_list[i] += 1
                flag = True
                break
            i += 1

        if flag == False:
            self.content_list.append(content)
            self.repeat_list.append(1)
            self.count +=1

    def __getitem__(self, index):
        return (self.repeat_list[index], self.content_list[index])

    def __len__(self):
        return self.count

class element_node:
    def __init__(self, tag, attrs, style_node, content = None, occur = 1):
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

    def is_leaf(self):
        return self.content is not None

    # functions __getitem__ and __len__
    # make ElementNode iterable.
    def __getitem__(self, index):
        return self.children[index]

    def __len__(self):
        return len(self.children)

    def add_new_elements(self, other):
        if len(other) == 0:
           pass
        else:
            flag = 0
            for s1 in self:   # iterate style nodes
                if s1 == other.children[0]:    # table-
                    flag = 1
                    s1.increment()
                    for e1, e2 in zip(s1, other.children[0]): #all children tags are equal
                        if e1.is_leaf() and e2.is_leaf(): #what if only one is leaf
                            e1.content.add_content(e2.content[0][1])
                        else:
                            e1.add_new_elements(e2)
            if flag == 0:
                self.children.append(other.children[0])

class page_tree:
    def __init__(self, url):
        # downloading and converting to DOM tree
        page_string = urllib2.urlopen(url)

        page_string = page_string.read() # remove breaks to be able to parse all text
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
        self.root = element_node('root', {}, [style_node([body_E])], None)

    def build_0(self, root): # takes e-tree node
        children = []

        for e in root.iterchildren():  # iterate etree object
            new_child = self.build_0(e)  # returns element nodes
            children.append(new_child)

        if len(root) == 0:
            if root.tag == 'img':
                temp = content_node()
                temp.add_content(root.attrib.get('src', None))
                return element_node(root.tag, root.attrib, children, temp)
            temp = content_node()
            temp.add_content(root.text)
            return element_node(root.tag, root.attrib, children, temp)

        return element_node(root.tag, root.attrib, children)

    def build_1(self, E):    # takes Element Node (root of SST/PST)
        E.children = [style_node(E.children)]
        for e in E.children[0].elements:
            self.build_1(e)

class style_tree:
    def __init__(self):
        self.root = element_node('root', {}, [])

    def add_page(self, page_tree):
        self.root.add_new_elements(page_tree.root)

def print_tree(root, level=0):
    ret = ("\t"*level) + print_Enode(root) + "\n"
    for style in root.children:
        for E in style.elements:
            ret += print_tree(E, level + 1)
    return ret

def print_Enode(root):
    count = []
    p = []
    for style in root.children:
        count.append((style.key, style.occur))

    if root.content is not None:
        for e in root.content:
            p.append(e)
        return "(%s, %s)" % (root.tag, p)
    return "(%s)" % (root.tag)