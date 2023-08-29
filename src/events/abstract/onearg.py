from abc import abstractmethod

from events.abstract.event import Event

class OneArg(Event):
    @abstractmethod
    def __init__(self, name : str, key : str):
        """These events accept a key as the sole argument.
        The key represents what data is stored by the event."""
        super().__init__(name, 1, f"<{key}>")
        self.key : str = key

    def parse(self, tokens : list[str]) -> dict:
        parent : dict = super().parse(tokens)
        # the sole token should be added as a value
        parent[self.key] = tokens,
        return parent
    
    def append(self, old : list, entry : dict) -> None:
        super().append(old, entry)
