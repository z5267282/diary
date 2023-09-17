import datetime as dt
import json
from os.path import basename
import sys

from config import DATE_FORMAT
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
        return NO_INPUT
    
    command : str = args.pop(0)
    match command:
        case "--help":
            display_help(events)
            return 0
        case "--prev":
            if not args:
                print("enter a command")
                return NO_INPUT
            
            shorthand : str = args.pop(0)
            return do_prev(shorthand, mapping)
    
    event : None | Event = mapping.get(command)
    if event is None:
        print(f"invalid command - '{command}'")
        return NO_COMMAND
    
    event.dump(args)
    return 0

def create_events():
    no_arg : list[Event] = [ BedLights(), Shave() ]
    one_arg : list[Event] = [ HairCut(), Note(), Ping() ]
    return no_arg + one_arg

def display_help(events : list[Event]):
    display_usage()
    print()
    print("events can be logged using the following shorthands:")
    print("\n".join(
        f"    {event.get_usage()}" for event in events
    ))

def display_usage():
    options : str = "[ --help ] | [ --prev shorthand ]"
    print(
        "usage : {} <shorthand> [ details ] | {}".format(
            basename(sys.argv[0]), options
        )
    )

def do_prev(shorthand : str, mapping : dict[str, Event]) -> int:
    event : None | Event = mapping.get(shorthand)
    if event is None:
        print(f"invalid shorthand - '{shorthand}'")
        return NO_COMMAND

    with open(event.get_filename(), "r") as f:
        entries : list[dict] = json.load(f)
    
    if not entries:
        print(f"there were no entries for {event.name}")
        return 0
    
    last      : str = event.prev(entries)
    last_time : dt.date = dt.datetime.strptime(last, DATE_FORMAT).date()
    today     : dt.date = dt.date.today()
    diff      : dt.timedelta = today - last_time
    print(f"it has been {diff.days} days since the last change to {shorthand}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
