'''
    Set of utilities to work with NTuples

    Created on 19 May 2014
    @author: kreczko
'''
from __future__ import print_function
from functools import total_ordering
from os.path import getsize
import json

from rootpy.io import root_open
from rootpy.tree import Tree

#from gecko.utils.json import JSONObject

class FileInfo( object ):
    def __init__( self, root_file_name ):
        self.name = root_file_name
        root_file = root_open(root_file_name)
        self.trees = []
        for path, _, objects in root_file.walk():
            for o in objects:
                full_path = path + '/' + o
                obj = root_file.Get( full_path )
                if 'Tree' in str( type( obj ) ):
                    self.trees.append( TreeInfo( obj, full_path ) )
        self.size = getsize( root_file_name )
        self.tree_size = sum( tree.size for tree in self.trees )
        self.tree_zipped_bytes = sum( tree.zipped_bytes for tree in self.trees )

    def toDict(self):
        d = {
            'class': str(self.__class__),
            'name': self.name,
            'size': self.size,
            'tree_size': self.tree_size,
            'tree_zipped_bytes': self.tree_zipped_bytes,
        }
        d['trees'] = {}
        for tree in self.trees:
            d['trees'][tree.name] = tree.toDict()
        return d


    def toJSON(self, output_file):
        output_file = open(output_file, 'w')
        output = json.dumps(self.toDict(), indent=4, sort_keys = True)
        output_file.write(output)
        output_file.close()

class TreeInfo( object ):
    def __init__( self, root_tree, full_path ):
        self.branches = []
        self.grouped_branches = {}
        self.name = root_tree.GetName()
        self.url = full_path
        self.n_branches = root_tree.GetNbranches()
        self.size = root_tree.get_tot_bytes()
        self.zipped_bytes = root_tree.get_zip_bytes()
        self.n_events = root_tree.GetEntriesFast()
        branches = sorted( list( root_tree.GetListOfBranches() ) )

        for branch in branches:
            self.addBranch(branch)
        self.compactifyGroups()

    def addBranch(self, root_branch):
        branch = BranchInfo( root_branch )
        group = branch.group
        if not self.grouped_branches.has_key( group ):
            self.grouped_branches[group] = BranchInfoGroup( group )
        self.grouped_branches[group].add( branch )
        self.branches.append(branch)

    def compactifyGroups(self):
        groups = self.grouped_branches.keys()
        #for name, g in self.grouped_branches.items():
        for group in groups:
            gd = BranchInfo.group_delimiter
            if gd in group:
                i = group.split(gd)
                parent = gd.join(i[:-1])
                g = self.grouped_branches[group]
                self.grouped_branches[parent].addGroup(g)
                self.grouped_branches.pop(group)


    def toDict(self):
        d = {
            'class': str(self.__class__),
            'name': self.name,
            'n_branches': self.n_branches,
            'n_events': self.n_events,
            'url': self.url,
            'size': self.size,
            'zipped_bytes': self.zipped_bytes,
        }
        d['collections'] = {}
        d['items'] = {}
        for group, info in self.grouped_branches.items():
            if info.is_collection():
                d['collections'][group] = info.toDict()
            else:
                d['items'][group] = info.toDict()
        return d

    @staticmethod
    def fromDict(dictionary):
        b = TreeInfo(None, '')
        b.name = dictionary['name']
        b.group = dictionary['group']
        b.size = dictionary['size']
        b.zipped_bytes = dictionary['zipped_bytes']
        return b

@total_ordering
class BranchInfo( object ):
    group_delimiter = '.'

    def __init__( self, root_branch = None):
        if root_branch is None:
            self.name = 'unknown'
            self.size = 0
            self.zipped_bytes = 0
            self.type = 'unknown'
        else:
            self.name = root_branch.GetName()
            self.size = root_branch.GetTotalSize()
            self.zipped_bytes = root_branch.GetZipBytes()
            self.type = Tree.branch_type(root_branch)

        self.subitems = {}
        if self.has_group():
            token = self.name.split( BranchInfo.group_delimiter )
            self.group = '.'.join(token[:-1])
        else:
            self.group = self.name

    def __eq__( self, other ):
        return ( ( self.name, self.size, self.zipped_bytes, self.group ) ==
                ( other.name, other.size, other.zipped_bytes, other.group ) )

    def __lt__( self, other ):
        return self.name < other.name

    def __str__( self ):
        s = 'Branch {0}: size = {1} bytes, zipped = {2} bytes}'
        return s.format( self.name, self.size, self.zipped_bytes )

    def has_group(self):
        return BranchInfo.group_delimiter in self.name

    def toDict(self):
        d = {
            'class': str(self.__class__),
            'name': self.name,
            'size': self.size,
            'zipped_bytes': self.zipped_bytes,
            'group': self.group,
            'type': self.type,
        }
        return d

    @staticmethod
    def fromDict(dictionary):
        b = BranchInfo()
        b.name = dictionary['name']
        b.group = dictionary['group']
        b.size = dictionary['size']
        b.zipped_bytes = dictionary['zipped_bytes']
        return b

    def is_collection(self):
        return 'vector' in str(self.type)

class BranchInfoGroup( object ):
    def __init__( self, name ):
        self.name = name
        self.branches = []
        self.groups = []

    def add( self, branch ):
        self.branches.append( branch )

    def addGroup(self, group):
        self.groups.append(group)

    def branches( self ):
        return self.branches

    @property
    def size( self ):
        return sum( [branch.size for branch in self.branches] )

    @property
    def zipped_bytes( self ):
        return sum( [branch.zipped_bytes for branch in self.branches] )

    def toDict(self):
        d = {
            'class': str(self.__class__),
            'name': self.name,
            'size': self.size,
            'zipped_bytes': self.zipped_bytes,
        }
        d['items'] = {}
        for branch in self.branches:
            d['items'][branch.name] = branch.toDict()
        d['groups'] = {}
        for group in self.groups:
            d['groups'][group.name] = group.toDict()
        return d

    @staticmethod
    def fromDict(dictionary):
        big = BranchInfoGroup(dictionary['name'])
        for _, branch in dictionary['items'].items():
            b = BranchInfo.fromDict(branch)
            big.add(b)
        return b

    def is_subgroup(self):
        return self.name.contains(BranchInfo.group_delimiter)

    def is_collection(self):
        return all([branch.is_collection() for branch in self.branches])
