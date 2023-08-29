from abc import abstractmethod

from event import Event

class NoArg(Event):
    @abstractmethod
    def __init__(self, name):
        super().__init__(name, 0)
