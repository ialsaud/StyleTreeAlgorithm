from SiteStyleTree import *
from math import log
"""
to calculate importance we look at two things:
    presentation style
    and content at the leaf nodes
"""



def NodeImp(E, occur):

    importance = 0
    if occur == 1:
        importance = 1
    else:
        for style in E.children: # child style
            p = (float(style.occur)/float(occur))
            importance -= p*( log(p)/log(occur) )
    return importance


def CompImp(E, occur):
    if len(E)==0:
        p = []
        for co in E.content:
            p.append(co)
        print "(%s, %s)" % (E.tag, p)
        if occur == 1:
            E.importance = 1
        else:
            sum =0
            for (occur_content, content) in E.content:
               sum += 1-(entropy(occur_content, occur))/float(1)

            E.importance = sum

    else:
        L = len(E.children)
        sum = 0
        for style in E:
            p = (float(style.occur)/occur)
            sum += p*CompImp_S(style)
        sum = sum*(0.9**L)

        E.importance = (1-(0.9**L))*NodeImp(E, occur) + sum

def entropy(occur_content, occur):
    sum = 0

    for i in range(occur):
        p1 = (float(occur_content)/float(occur))
        p = p1*((1-p1)**(i))
        i += 1
        print p
        sum += p*(log(p)/log(occur))
    return (-sum)

def CompImp_S(style):
    sum = float(0)
    for e in style:
        sum += CompImp(e, style.occur)

    return sum/len(style)

