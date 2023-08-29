from abc import ABC, abstractmethod

from event import Event

class NoArg(Event):
    @abstractmethod
    def __init__(self, name):
        super().__init__(name, 0)
    
    @abstractmethod
    def tokenise(self, data : str) -> list[str]:
        tokens : list[str] = super().tokenise(data)
        if tokens:
            raise ValueError(f"{self.name} expects no arguments")
        return tokens
