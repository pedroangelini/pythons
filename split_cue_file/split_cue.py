from itertools import pairwise
import re

FILE_NAME = "In Times Like These_ Mega Boxed Set [B09Z74TD4Z].cue"
FRAMERATE = 75.0
SPLITS = (27, 61)


with open(FILE_NAME, "r") as fp:
    cue_content = fp.read()

first_line = cue_content[0 : cue_content.find("\n")]
tracks_content = cue_content[cue_content.find("\n") :]


def time_str_to_s(timestr: str) -> float:
    minutes, sec, frames = timestr.split(":")
    minutes = int(minutes)
    sec = int(sec)
    frames = int(frames)

    return minutes * 60 + sec + frames / FRAMERATE


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


blocklist = re.findall("((?:[^\n]+\n?){1,3})", tracks_content)

tracks: list[Track] = []
for block in blocklist:
    tracks.append(Track.from_str(block))

with open("track_list.txt", "w") as fp:
    fp.write("\n".join([str(t) for t in tracks]))


splits = [0, *SPLITS, max([t.num for t in tracks])]
splits = list(pairwise(splits))
print("Book boundaries:", splits)

time_boundaries = [tracks[s - 1].time_s for s in SPLITS]
print(time_boundaries)
# print("\n".join([str(t.offset_time_s(-10)) for t in tracks[0:2]]))
