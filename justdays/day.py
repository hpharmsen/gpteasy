from __future__ import annotations
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import calendar

DATE_FORMAT = "%Y-%m-%d"


class Day:
    def __init__(self, *args):
        """Day can be intialized with:"""
        if len(args) == 3:
            """Three arguments: year, month, day"""
            dt = datetime(*args)
        elif len(args) == 2:  # year, week
            """Two arguments: year, week. Day with be the Monday of that week"""
            dt = datetime.strptime(f"{args[0]} {args[1]} 1", "%Y %W %w")
        elif len(args) == 0:
            """No arguments: today"""
            dt = datetime.today()
        elif isinstance(args[0], str):
            """One argument: string in format YYYY-MM-DD"""
            y, m, d = args[0].split("-")
            dt = datetime(int(y), int(m), int(d))
        elif isinstance(args[0], (date, datetime)):
            """One argument: datetime or date"""
            dt = args[0]
        else:
            raise f"Invalid type passed to Day class: {args[0]} with type {type(args[0])}"
        self.str = dt.strftime(DATE_FORMAT)
        self.d, self.m, self.y = dt.day, dt.month, dt.year

    def __str__(self) -> str:
        return self.str

    def __repr__(self) -> str:
        return f"Day({self.str})"

    def __hash__(self):
        return hash(self.str)

    def __lt__(self, other) -> bool:
        return str(self) < str(other)

    def __gt__(self, other) -> bool:
        return str(self) > str(other)

    def __le__(self, other) -> bool:
        return str(self) <= str(other)

    def __ge__(self, other) -> bool:
        return str(self) >= str(other)

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __sub__(self, other) -> int:
        """Days can be substracted from each other"""
        return (self.as_datetime() - other.as_datetime()).days

    def as_datetime(self) -> datetime:
        return datetime(self.y, self.m, self.d)

    def as_date(self) -> date:
        return date(self.y, self.m, self.d)

    def as_unix_timetamp(self) -> int:
        """Returns the unix timestamp of the day"""
        return int(self.as_datetime().timestamp())

    def strftime(self, date_format: str) -> str:
        """Works just like the strftime from datetime"""
        return self.as_datetime().strftime(date_format)

    def next(self) -> Day:
        """Returns the next day"""
        return self.plus_days(1)

    def next_weekday(self) -> Day:
        """Returns the first day in the future that is on a weekday"""
        day = self.plus_days(1)
        while day.day_of_week() >= 5:
            day = day.plus_days(1)
        return day

    def prev(self) -> Day:
        """Return the previous day"""
        return self.plus_days(-1)

    def plus_days(self, increment) -> Day:
        """Returns a new Day object increment days further in the future"""
        return Day(self.as_datetime() + timedelta(days=increment))

    def plus_weeks(self, increment) -> Day:
        """Returns a new Day object increment weeks further in the future"""
        return Day(self.as_datetime() + relativedelta(weeks=increment))  # relativedelta

    def plus_months(self, increment) -> Day:
        """Returns a new Day object increment months further in the future"""
        return Day(
            self.as_datetime() + relativedelta(months=increment)
        )  # relativedelta

    def is_weekday(self) -> bool:
        """Returns True if day is a weekday (Monday to Friday)"""
        return self.as_datetime().weekday() < 5

    def is_weekend(self) -> bool:
        """Returns True of day is a Saturday or Sunday."""
        return self.as_datetime().weekday() >= 5

    def day_of_week(self) -> int:
        """Return day of the week, where Monday == 0 ... Sunday == 6."""
        return self.as_datetime().weekday()

    def week_number(self) -> int:
        """Return the week number of the year."""
        return self.as_datetime().isocalendar().week

    def day_of_the_year(self) -> int:
        """Day of the year is a number between 1 and 365/366, January 1st is day 1"""
        return self.as_datetime().timetuple().tm_yday

    def fraction_of_the_year_past(self) -> float:
        """Returns a fraction of how much of the year is past including the current day"""
        is_leap_year = self.y % 4 == 0 and (self.y % 100 != 0 or self.y % 400 == 0)
        return self.day_of_the_year() / (366 if is_leap_year else 365)

    def last_monday(self) -> Day:
        """Returns the last day that was a Monday or the day itself if it is a Monday"""
        return self.plus_days(-self.as_datetime().weekday())

    def last_day_of_month(self) -> Day:
        """Returns the last day of the month"""
        return Day(self.y, self.m, calendar.monthrange(self.y, self.m)[1])
