import inspect

class Node():
    def __init__(self, tag, attrs, children):
        self.tag = tag
        self.attrs = attrs
        self.children = children

    def get_dict(self):
        x = {}
        for child in self.children:
            if child.tag.__str__() is not '':
                x.update(child.get_dict())
        return {self.tag: x}

    def __repr__(self):
        return "not implemented"



"""
print child.tag
if '__get__' in dir(child.tag):
    print "IM IN!!!"
    print child.tag.__str__()

#print dir(child.tag)
"""