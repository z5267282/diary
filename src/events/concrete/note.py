from events.abstract.onearg import OneArg

class Note(OneArg):
    def __init__(self):
        super().__init__("note", "details")
