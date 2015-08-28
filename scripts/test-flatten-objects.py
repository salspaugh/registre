import inspect
import registre.featurize

class Foo(object):
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Bar(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

foo1 = Foo(1, 'a', Bar(8, 9))
foo2 = Foo(2, 'b', Bar(6, 7))

print hasattr(foo1, "__dict__")

features = registre.featurize.get_possible_features([foo1, foo2])
for (var, domain) in features.iteritems():
    print var, domain
