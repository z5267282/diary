from events.abstract.onearg import OneArg

class Ping(OneArg):
    def __init__(self):
        super().__init__("ping", "person")
