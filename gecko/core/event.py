'''
    This is where the magic happens
'''

class EventModel(TreeModel):
    pass

class HEPEvent():
    def __init__(self):
        pass
        
    def passes(self, selection):
        '''
            This function only exists in order to make the resulting syntax
            more like English:
            event = Event()
            event.passes(Selection)
            If I could, I would add an '?' ;)
            But it is also important that the selection instance exists outside
            of the event, since a global total cut flow is needed.
        '''
        return selection(event)
