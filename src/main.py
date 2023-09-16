from os.path import basename
import sys

from error import NO_INPUT, NO_COMMAND

from events.abstract.event import Event

# no arg
from events.concrete.bedlights import BedLights
from events.concrete.shave import Shave
# one arg
from events.concrete.haircut import HairCut
from events.concrete.note import Note
from events.concrete.ping import Ping

def main():
    events : list[Event] = create_events()
    mapping : dict[str, Event] = {
        event.get_shorthand() : event for event in events
    }

    args = sys.argv[1:]
    if not args:
        print("enter a command")
        sys.exit(NO_INPUT)
    
    command : str = args.pop(0)
    if command == "--help":
        display_help(events)
        sys.exit(0)
    
    event : Event = mapping.get(command)
    if event is None:
        print(f"invalid command - '{command}'")
        sys.exit(NO_COMMAND)
    
    event.dump(args)

def create_events():
    no_arg : list[Event] = [ BedLights(), Shave() ]
    one_arg : list[Event] = [ HairCut(), Note(), Ping() ]
    return no_arg + one_arg

def display_help(events : list[Event]):
    print(f"usage : {basename(sys.argv[0])} [ -[p]rev command ]")
    print()
    print("these things can be logged")
    print("\n".join(
        f"    {event.get_usage()}" for event in events
    ))

if __name__ == "__main__":
    main()
