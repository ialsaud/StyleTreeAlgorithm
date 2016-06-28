from SiteStyleTree import *


x1 = PageTree('http://www.securityfocus.com/bid/83265')
#x2 = PageTree('http://www.securityfocus.com/bid/83265')
#x3 = PageTree('http://www.securityfocus.com/bid/69077')

def printpage(page):
    print "__________"
    print page
    for e in page.children:
        print "child:"
        if e is not None:
            print e
            for r in e.elements:
                printpage(r)

