from SiteStyleTree import *


def print_tree(root, level=0):
    ret = ("\t"*level) + print_enode(root) + "\n"
    for style in root.children:
        for E in style.elements:
            ret += print_tree(E, level + 1)
    return ret


def print_enode(root):
    count = []
    for style in root.children:
        count.append((style.key, style.occur))
    if root.content is not None:
        return "(%s, %s, %s)" % (root.tag, count, root.content)
    return "(%s, %s)" % (root.tag, count)


x1 = PageTree('http://www.securityfocus.com/bid/83265')
x2 = PageTree('http://www.securityfocus.com/bid/83265')
print print_tree(x2.root)


SST = StyleTree()
SST.add_page(x1)
SST.add_page(x2)
print(print_tree(SST.root))

# print SST.children[0].occur
