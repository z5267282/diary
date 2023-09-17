from abc import ABC, abstractmethod
from datetime import datetime
import json
import os
import sys

from config import DATE_FORMAT, LOGS
from error import BAD_ARGS

class Event(ABC):
    DATE_KEY : str = "date"

    @abstractmethod
    def __init__(self, name : str, num_args : int, usage : str):
        """Note that subclasses must eventually call a concrete constructor"""
        # the full name in lowercase with spacebars if needed
        self.name : str = name 
        self.num_args : int = num_args
        self.usage : str = usage
    
    def get_shorthand(self) -> str:
        """Convert the full name into a shorthand.
        For one word names this should be the first and last letter.
        Shorthands should be the first letter in each word of the full name."""
        tokens : list[str] = self.name.split(" ")
        match len(tokens):
            case 1:
                return self.name[0] + self.name[-1]
            case _:
                return "".join(t[0] for t in tokens)

    def dump(self, tokens : list[str]) -> None:
        try:
            entry : dict = self.parse(tokens)
        except ValueError as error:
            print(error, file=sys.stderr)
            sys.exit(BAD_ARGS)

        filename : str = self.get_filename()
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                json.dump([], f, indent=2)

        with open(filename, "r") as f:
            old : list = json.load(f)
            self.append(old, entry)
        
        with open(filename, "w") as f:
            json.dump(old, f, indent=2)
    
    @abstractmethod
    def parse(self, tokens : list[str]) -> dict:
        """Parse raw input into an event in dictionary format.
        Raise a ValueError if an error occurred"""
        if len(tokens) != self.num_args:
            raise ValueError("{} expects {} argument{}".format(
                self.name, self.num_args,
                "" if self.num_args == 1 else "s"
            ))
        today = datetime.now().strftime(DATE_FORMAT)
        return { Event.DATE_KEY : today }
    
    @abstractmethod
    def append(self, old : list, entry : dict) -> None:
        pass

    def prev(self, entries : list[dict]) -> str:
        return entries[-1][Event.DATE_KEY]
    
    def get_filename(self) -> str:
        """Filenames should be hyphenated version with .json as a suffix"""
        js : str = "{}.json".format(self.name.replace(" ", "-"))
        return os.path.join(LOGS, js)
    
    def get_usage(self) -> str:
        return f"{self.get_shorthand()} : {self.name} {self.usage}"
