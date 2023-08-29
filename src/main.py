import sys

from error import NO_INPUT, NO_COMMAND

from events.abstract.event import Event

from events.concrete.bedlights import BedLights
from events.concrete.shave import Shave

def main():
    events : list[Event] = [
        BedLights(), Shave()
    ]
    mapping : dict[str, Event] = {
        event.get_shorthand() : event for event in events
    }

    args = sys.argv[1:]
    if not args:
        print("enter a command")
        sys.exit(NO_INPUT)
    
    command : str = args.pop(0)
    if command == "--help":
        print("these things can be logged")
        print("\n".join(
            f"    {event.get_usage()}" for event in events
        ))
        sys.exit(0)

    event : Event = mapping.get(command)
    if event is None:
        print(f"invalid command - '{command}'")
        sys.exit(NO_COMMAND)
    
    event.dump(args)

if __name__ == "__main__":
    main()
