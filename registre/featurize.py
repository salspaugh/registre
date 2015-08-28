import collections
import inspect

def get_all_attributes(klass):
    attrs = inspect.getmembers(klass, lambda a:not(inspect.isroutine(a)))
    orig = [a for a in attrs if not a[0].startswith('_')]
    final = []
    for (attr, val) in orig:
        if hasattr(val, "__iter__"):
            item_attrs = []
            for item in val:
                if hasattr(item, "__dict__"):
                    item_attrs.extend(get_all_attributes(item))
            final.extend(item_attrs)
        elif hasattr(val, "__dict__"):
            final.extend(get_all_attributes(val))
        else:
            final.append((attr, val))
    return final

def get_possible_features(klasses):
    features = collections.defaultdict(set)
    for klass in klasses:
        attributes = get_all_attributes(klass)
        for (attr, val) in attributes:
            if type(val) == type({}): continue # no dict-typed features (?)
            if type(val) == type([]): val = tuple(val)
            features[attr].add(val)
    return features
