'''
An MetaClass (or rather base?) for all selections
Inherits from Callable (has to implement __call__), takes an event as parameter.
Evaluates for all selection steps if event passes and records the result.
For final result can use all() on the list of selection step results.

A selection is meant to be kept alive for the entire event loop, meaning that it
will contain the full cut flow.
'''

class SelectionBase(type):

    def __init__(self):
        self.selection_steps = ordered_list()

    def __call__(self, event):
        pass

class SelectionStepMeta(type):
    '''
        needs to define:
        - event attribute to use
        - cut value
        - operator to use
    '''
    def __init__(self):
        self.name

    def __call__(self, event):
        pass
