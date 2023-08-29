from abc import abstractmethod

from events.abstract.event import Event

class NoArg(Event):
    @abstractmethod
    def __init__(self, name):
        """No arg events are to be run without arguments"""
        super().__init__(name, 0)
    
    def append(self, old: list, entry: dict) -> None:
        """No arg events should only store their date"""
        old.append(entry["date"])
