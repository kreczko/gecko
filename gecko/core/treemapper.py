from __future__ import nested_scopes
import rootpy


def delegate(attribute_name, method_names):
    def decorator(cls):
        #nonlocal attribute_name # works only in python3
        # workaround for python 2.x
        a = attribute_name
        if a.startswith('__'):
            a = '_' + cls.__name__ + a
        for name in method_names:
            func_dsc ='lambda self, *a, **kw: self.{0}.{1}(*a, **kw)'
            func_dsc = func_dsc.format(a, name)
            setattr(cls, name, eval(func_dsc))
        return cls
    return decorator

@delegate('__tree', ['__iter__'])
class TreeMapper():

    def __init__(self, tree, mapping):
        self.__tree = tree
        self.__mapping = mapping
        #print self.__dict__

    def __getattr__(self, attr):
        if attr in ['__tree', '__mapping']:
            return self.__dict__[attr]
        new_attr = attr
        if attr in self.__dict__['_TreeMapper__mapping'].keys():
            new_attr = self.__dict__['_TreeMapper__mapping'][attr]
        return self.__tree.__getattr__(new_attr)

    def __iter__(self):
        yield(TreeMapper(self.__tree.__iter__(), self.__mapping))

#    def __setattr__(self, attr, value):
#        if attr in ['__tree', '__mapping']:
#            self.__dict__[attr] = value
#            return
#        new_attr = attr
#        if attr in self.__dict__['__mapping'].keys():
#            new_attr = self.__dict__['__mapping'][attr]
#        self.__tree.__setattr__(new_attr, value)
