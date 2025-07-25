import argparse
from dataclasses import dataclass
from enum import Enum, StrEnum, auto
import sys


class States:
    in_book = auto()
    in_gap = auto()


state = States.in_book
gap_seconds = 0.0


def time_float_to_str(timefloat: float) -> str:
    minutes = int(timefloat / 60)
    sec = int(timefloat - minutes * 60)
    frames = int((timefloat - int(timefloat)) * 75)

    return f"{minutes}:{sec}:{frames}"


class Track:
    def __init__(self, num, title, time_s):
        self.num = num
        self.title = title
        self.time_s = time_s

    @classmethod
    def from_str(self, three_line_string: str):
        lines = three_line_string.splitlines()
        num = int(lines[0].split(" ")[1])
        title = lines[1][8:].strip('"')
        time_s = time_str_to_s(lines[2].strip().split(" ")[2])
        return Track(num, title, time_s)

    def __str__(self):
        return f"{self.num} - {self.title} - {self.time_s}"

    def __repr__(self):
        return f"{self.num} - {self.title} - {self.time_s}"

    def str_block(self):
        timestr = time_float_to_str(self.time_s)
        return f"""TRACK {self.num} AUDIO
  TITLE "{self.title}"
  INDEX 01 {timestr}
"""

    def offset_time_s(self, offset):
        self.time_s = self.time_s + offset
        return self


class EventType(StrEnum):
    T = "T"
    E = "E"
    S = "S"


@dataclass
class Event:
    ts: float
    event_type: EventType
    title: str


def parse_events_file(input_file: str) -> list[Event]:
    el = []
    try:
        with open(input_file, "r") as fp:
            content = fp.read().splitlines()
        for line in content:
            typ, title, sec = line.split(" - ")
            event = Event(ts=float(sec), event_type=EventType(typ), title=title.strip())
            el.append(event)
    except Exception as e:
        print(f"Could not parse file: {str(e)}", file=sys.stderr)

    return el


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates a CUE file based on a list of tracks, starts and ends"
    )
    parser.add_argument("-i", "--input", help="input file name", required=True)
    parser.add_argument("-o", "--output", help="output file name", required=True)
    args = parser.parse_args()

    events = parse_events_file(args.input)
    print(events)
