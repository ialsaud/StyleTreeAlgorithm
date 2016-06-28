from SiteStyleTree import *

def print_PST(root, level=0):
    ret = ("\t"*level) + print_Enode(root) + "\n"
    for style in root.children:
        for E in style.elements:
            ret += print_PST(E, level+1)
    return ret

def print_Enode(root):
    count = []
    for style in root.children:
        count.append((style.key,style.occur))
    return "(%s, %s)" % (root.tag, count)

PST = PageTree('http://www.securityfocus.com/bid/83265')
print print_PST(PST.root)


#SST = StyleTree()
#SST.add_page(PST)


##print SST.children[0].occur


