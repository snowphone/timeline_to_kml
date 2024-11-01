from pydantic import BaseModel
from datetime import datetime


class Activity(BaseModel):
    class Inner(BaseModel):
        class Loc(BaseModel):
            latLng: str

        start: Loc
        end: Loc

    startTime: datetime
    endTime: datetime
    startTimeTimezoneUtcOffsetMinutes: int | None
    endTimeTimezoneUtcOffsetMinutes: int | None
    activity: Inner


class TimelinePath(BaseModel):
    class PT(BaseModel):
        point: str
        time: datetime

    startTime: datetime
    endTime: datetime
    timelinePath: list[PT]


class TimelineMemory(BaseModel):
    startTime: datetime | None
    endTime: datetime | None
    startTimeTimezoneUtcOffsetMinutes: int | None = None
    endTimeTimezoneUtcOffsetMinutes: int | None = None
    timelineMemory: dict  # no location info


class Visit(BaseModel):
    class Inner(BaseModel):
        class Loc(BaseModel):
            class PT(BaseModel):
                latLng: str

            placeLocation: PT

        topCandidate: Loc

    startTime: datetime
    endTime: datetime
    startTimeTimezoneUtcOffsetMinutes: int
    endTimeTimezoneUtcOffsetMinutes: int
    visit: Inner


class Timeline(BaseModel):
    semanticSegments: list[Activity | TimelinePath | TimelineMemory | Visit]
    rawSignals: list
    userLocationProfile: dict
