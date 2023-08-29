from abc import ABC, abstractmethod
from datetime import datetime
import json
    
class Event(ABC):
    def __init__(self, name : str):
        # the full name in lowercase with spacebars if needed
        self.name : str = name 
    
    def get_filename(self) -> str:
        """Filenames should be hyphenated version with .json as a suffix"""
        return "{}.json".format(self.name.replace(" ", "-"))
    
    def get_shorthand(self) -> str:
        """Convert the full name into a shorthand.
        For one word names this should be the first and last letter.
        Shorthands should be the first letter in each word of the full name."""
        tokens : list[str] = self.name.split(" ")
        match len(tokens):
            case 1:
                return self.name[0] + self.name[-1]
            case _:
                return " ".join(t[0] for t in tokens)

    @abstractmethod
    def parse(self, data : str) -> dict:
        today = datetime.now().strftime('%d/%m/%Y')
        return { "date" : today }
    
    @abstractmethod
    def append(self, old : list, entry : dict) -> None:
        pass
    
    def dump(self, data : str) -> None:
        with open(self.get_filename(), "r") as f:
            old : list = json.load(f)
            entry : dict = self.parse(data)
            self.append(old, entry)
        
        with open(self.get_filename(), "w") as f:
            json.dump(old, f)
