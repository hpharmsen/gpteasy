import pytest
from justdays import Day, Period


@pytest.fixture
def the_day() -> Day:
    return Day('2022-12-30')


@pytest.fixture
def next_monday() -> Day:
    return Day('2023-01-02')


@pytest.fixture
def the_period(the_day: Day, next_monday: Day) -> Period:
    return Period(the_day, next_monday)


@pytest.fixture
def open_period(the_day: Day) -> Period:
    return Period(the_day)


# Initializing a Period
def test_init_strings(the_period: Period):
    assert Period('2022-12-30', '2023-01-02') == the_period


# Accessing Period fields
def test_fromday(the_period: Period, the_day: Day):
    assert the_period.fromday == the_day


def test_untilday(the_period: Period, next_monday: Day):
    assert the_period.untilday == next_monday


def test_fromday_open(open_period: Period, the_day: Day):
    assert open_period.fromday == the_day


def test_untilday_open(open_period: Period):
    assert open_period.untilday is None


def test_len(the_period: Period):
    assert len(the_period) == 3


# Iterating over a Period
def test_iter(the_period: Period, the_day: Day, next_monday: Day):
    assert list(the_period) == [the_day, the_day.next(), next_monday.prev()]


# Checking if a Day falls within a Period
def test_contains_day(the_period: Period, the_day: Day):
    assert the_day in the_period


def test_contains_day_open(open_period: Period, the_day: Day):
    assert the_day in open_period


def test_contains_not_day(the_period: Period, next_monday: Day):
    assert next_monday not in the_period


def test_contains_period(the_period: Period, the_day: Day):
    assert Period(the_day, the_day.next()) in the_period


def test_contains_not_period(the_period: Period, the_day: Day):
    assert Period(the_day, the_day.plus_weeks(1)) not in the_period


def test_contains_period_open(open_period: Period, the_day: Day):
    assert Period(the_day, the_day.next()) in open_period


def test_open_period_contains_open_period(open_period: Period, next_monday: Day):
    assert Period(next_monday) in open_period


def test_period_from_week():
    period = Period.from_week(2022, 36)
    assert Day(2022, 9, 4) not in period
    assert Day(2022, 9, 5) in period
    assert Day(2022, 9, 11) in period
    assert Day(2022, 9, 12) not in period


def test_period_from_month():
    period = Period.from_month(2022, 8)
    assert Day(2022, 7, 31) not in period
    assert Day(2022, 8, 1) in period
    assert Day(2022, 8, 31) in period
    assert Day(2022, 9, 1) not in period
