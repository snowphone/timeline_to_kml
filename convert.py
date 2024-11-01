import argparse
import simplekml

import re
from pydantic import BaseModel
from datetime import datetime
from model import Activity, Timeline, TimelineMemory, TimelinePath, Visit

from functools import singledispatch
import tqdm


class Pos(BaseModel):
    time: datetime
    loc: tuple[str, str]


@singledispatch
def get_locations(_) -> list[Pos]: ...


def parse(loc: str):
    pattern = re.compile(r"(.*)°, (.*)°")
    m = pattern.match(loc)
    assert m
    return (
        (m.group(2)),
        (m.group(1)),
    )


@get_locations.register
def _(it: Activity):
    return [
        Pos(time=it.startTime, loc=parse(it.activity.start.latLng)),
        Pos(time=it.endTime, loc=parse(it.activity.end.latLng)),
    ]


@get_locations.register
def _(it: TimelinePath):
    return [Pos(time=jt.time, loc=parse(jt.point)) for jt in it.timelinePath]


@get_locations.register
def _(_: TimelineMemory):
    return []


@get_locations.register
def _(it: Visit):
    loc = parse(it.visit.topCandidate.placeLocation.latLng)
    return [
        Pos(time=it.startTime, loc=loc),
        Pos(time=it.endTime, loc=loc),
    ]


def main(args: argparse.Namespace):
    with open(args.input) as f:
        timeline = Timeline.model_validate_json(f.read())

    kml = simplekml.Kml(name="Timeline")

    iter = tqdm.tqdm(timeline.semanticSegments) if args.progress else timeline.semanticSegments

    for history in iter:
        locs = get_locations(history)

        for loc in locs:
            timestr = loc.time.isoformat()
            point = kml.newpoint(name=timestr)
            point.coords = [loc.loc]
            point.timestamp.when = timestr

    kml.save(args.output)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", help="Timeline.json path", required=True)
    parser.add_argument("--output", help="path_to_kml", required=True)
    parser.add_argument("--progress", action='store_true')
    main(parser.parse_args())
