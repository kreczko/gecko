from rootpy.vector import LorentzVector

class Particle(object):
    def __init__(self):
        self.__fourvector = LorentzVector()

class Jet(Particle):
    pass

class GenJet(Particle):
    pass

class Electron(Particle):
    pass

class Muon(Particle):
    pass

class Tau(Particle):
    pass

class Photon(Particle):
    pass

class Track(object):
    pass

class Trigger(object):
    pass
