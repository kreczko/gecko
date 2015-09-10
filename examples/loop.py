from __future__ import print_function
from rootpy.io import File

file_name = '/storage/TopQuarkGroup/TTJets_Madgraph_PU20bx25_001.root'

f = File(file_name)
tree = f.Get('nTupleTree/tree')

mapping = {'Time': 'Event.Time'}
from gecko.core.treemapper import TreeMapper
t = TreeMapper(tree, mapping)
print(type(tree))
i = 0
for event in t:
    e = TreeMapper(event, mapping)
    #print(dir(event))
    print(event.__getattr__('Event.Time'))
    print(e.Time)
    break
