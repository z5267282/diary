from events.abstract.onearg import OneArg

class HairCut(OneArg):
    def __init__(self):
        super().__init__("haircut", "location")
