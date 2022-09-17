from __future__ import annotations

from .day import Day


class Period:
    """Bundles a startdate and optionally an end date to form a date range"""

    def __init__(self, fromday, untilday=None):
        """Period is initalized with a startdate and optionally an end date
        Start date can be a Day object or a string in the format 'YYYY-MM-DD'"""
        if not isinstance(fromday, Day):
            fromday = Day(fromday)
        self.fromday = fromday
        if untilday and not isinstance(untilday, Day):
            untilday = Day(untilday)
        self.untilday = untilday
        self.current = fromday.prev()  # Initialize iterator

    def __str__(self) -> str:
        return f'{self.fromday} --> {self.untilday if self.untilday else ""}'

    def __repr__(self) -> str:
        return f"Period({str(self)})"

    def __hash__(self):
        return hash(str(self))

    def __iter__(self) -> Period:
        return self

    def __next__(self) -> Day:
        self.current = self.current.next()
        if self.current == self.untilday:
            raise StopIteration
        return self.current

    def __contains__(self, other: Day | Period) -> bool:
        if type(other) == Day:
            return self.fromday <= other < self.untilday
        elif type(other) == Period:
            if not self.untilday:
                return self.fromday <= other.fromday
            if not other.untilday:
                return False
            return self.fromday <= other.fromday < self.untilday and self.fromday <= other.untilday < self.untilday
        raise TypeError(f"Invalid type passed to Period.__contains__: {type(other)}")

    def __len__(self) -> int:
        return self.untilday - self.fromday

    def __eq__(self, other) -> bool:
        return self.fromday == other.fromday and self.untilday == other.untilday
