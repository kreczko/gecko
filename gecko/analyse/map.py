'''
    module to determine the input of the analyse

    DEV description
    the idea is to be able to create an Event model class from a Tree.
    For this it is best to use TreeModel together with an automated definition of variables.
    In other words:
    We want this behaviour: create a class from a data input  (kind of what protobuf would do)
    Event = map.define_event(tree, branches = ['Event.run', 'cleanPatJetsAK5PF'])

    tree = rootpy.tree.Tree("name_of_tree", model=Event) # for writing
    map.set_up_tree(tree, aliases = {'cleanPatJetsAK5PF': 'jets'}) # for reading
    # such that
    for event in tree:
        print(event.run) # for Event.run
        jets = event.jets # for cleanPatJetsAK5PF
        for jet in jets:
            jet.pt() # from cleanPatJetsAK5PF[i].pt
            jet.genJet.pt() # from cleanPatJetsAK5PF[i].GenJet.Pt
            jet.eta() # from Jet fourvector (from cleanPatJetsAK5PF[i].px, py, pz, energy)
        event.passes(TopPairMuonSelection) # passes is an extension to the TreeModel, selection is a Callable
        # also, if already applied, this should be cached information; i.e. Event.passesTopPairMuonSelection exists or
        # event.passes(TopPairMuonSelection) has been called before.
        if event.has_applied(modify.smearPt):
            unsmeared_jets = event.unsmeared_jets # if smearing has been applied, these are the original cleanPatJetsAK5PF[i]


    'Event.run' should be mapped to the event itse
'''

class MapperMeta(type)
    ''' Meta class for Mapper'''
