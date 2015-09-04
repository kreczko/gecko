'''
    module to modify inputs.
    Example:
    smearPt(jets, smearFactors)
    applyScaleFactor(electrons, electronSFs)
    In short: takes an input collection and modifies it given a set of rules
    This provides 1 to 1 mapping, nothing is dropped. This can be seen as an
    extension to mapping step (e.g. smearPt) but in reality some of them might run _after_
    the filter step (applyScaleFactor, since it is an event weight)

'''
