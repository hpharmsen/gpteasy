import datetime
import pytest
from justdays import Day


@pytest.fixture
def the_day() -> Day:
    return Day('2022-12-30')


@pytest.fixture
def next_monday() -> Day:
    return Day('2023-01-02')

# Initializing a Day
def test_init():
    assert Day().as_date() == datetime.date.today()


def test_init_string():
    assert Day('2022-12-30').as_date() == datetime.date(2022, 12, 30)


def test_init_year_week():
    assert Day(2022, 37).as_date() == datetime.date(2022, 9, 12)


def test_init_year_month_day():
    assert Day(2022, 12, 30).as_date() == datetime.date(2022, 12, 30)


def test_init_datetime():
    assert Day(datetime.datetime(2022, 12, 30)) == Day('2022-12-30')


def test_init_date():
    assert Day(datetime.date(2022, 12, 30)) == Day('2022-12-30')


# Accessing Day fields
def test_d(the_day: Day):
    assert the_day.d == 30


def test_m(the_day: Day):
    assert the_day.m == 12


def test_y(the_day: Day):
    assert the_day.y == 2022


def test_string(the_day: Day):
    assert the_day.str == '2022-12-30'


# Represenation
def test_str(the_day: Day):
    assert str(the_day) == '2022-12-30'


def test_as_datetime(the_day: Day):
    assert the_day.as_datetime() == datetime.datetime(2022, 12, 30)


def test_strftime(the_day: Day):
    format_string = '%A %d %B %Y'
    assert the_day.strftime(format_string) == 'Friday 30 December 2022'


def test_as_unix_timestamp(the_day: Day):
    assert the_day.as_unix_timestamp() == datetime.datetime(2022, 12, 30).timestamp()


# Days further away or in the past
def test_next(the_day: Day):
    assert the_day.next() == Day('2022-12-31')


def test_previous(the_day: Day):
    assert the_day.prev() == the_day - 1


def test_add_int(the_day: Day):
    assert the_day + 3 == Day(2023, 1, 2)


def test_add_int_right(the_day: Day):
    assert 3 + the_day == Day(2023, 1, 2)


def test_add_float():
    with pytest.raises(TypeError):
        Day() + 1.0


def test_substract_day(the_day: Day, next_monday: Day):
    assert next_monday - the_day == 3


def test_substract_int(the_day: Day, next_monday: Day):
    assert next_monday - 3 == the_day


def test_substract_float():
    with pytest.raises(TypeError):
        Day() - 1.0


def test_next_weekday(the_day: Day):
    assert the_day.next_weekday() == Day('2023-01-02')


def test_next_weekday_on_a_monday(next_monday: Day):
    assert next_monday.next_weekday() == Day('2023-01-03')


def test_next_weekday_on_a_sunday(next_monday: Day):
    assert Day('2023-01-01').next_weekday() == next_monday


def test_plus_weeks(the_day: Day):
    assert the_day.plus_weeks(2) == Day('2023-01-13')


def test_plus_months_1(the_day: Day):
    assert the_day.plus_months(1) == Day('2023-01-30')


def test_plus_months_2(the_day: Day):
    assert the_day.plus_months(2) == Day('2023-02-28')


# Comparing days
def test_greater_than(the_day: Day, next_monday: Day):
    assert next_monday > the_day


def test_greater_equal(the_day: Day, next_monday: Day):
    assert next_monday >= the_day


def test_less_than(the_day: Day, next_monday: Day):
    assert the_day < next_monday


def test_less_equal(the_day: Day, next_monday: Day):
    assert the_day <= next_monday


def test_days_difference(the_day: Day, next_monday: Day):
    assert next_monday - the_day == 3


def test_days_difference_negative(the_day: Day, next_monday: Day):
    assert the_day - next_monday == -3


# Miscellaneous
def test_is_weekend(the_day: Day):
    assert not the_day.is_weekend()


def test_is_weekday(the_day: Day):
    assert the_day.is_weekday()


def test_day_of_week(the_day: Day):
    assert the_day.day_of_week() == 4


def test_day_of_year(the_day: Day):
    assert the_day.day_of_year() == 364


def test_fraction_of_the_year_past(the_day: Day):
    assert the_day.fraction_of_the_year_past() == 364 / 365


def test_week_number(the_day: Day):
    assert the_day.week_number() == 52


def test_last_monday(the_day: Day):
    assert the_day.last_monday() == Day('2022-12-26')


def test_last_monday_on_a_monday(next_monday: Day):
    assert next_monday.last_monday() == next_monday


def test_last_day_of_month(the_day: Day):
    assert the_day.last_day_of_month() == Day('2022-12-31')


def test_last_day_of_month_feb():
    assert Day('2022-02-02').last_day_of_month() == Day('2022-02-28')


def test_add_str(the_day: Day):
    assert the_day + ' is the day' == '2022-12-30 is the day'


def test_add_str_right(the_day: Day):
    assert 'date: ' + the_day == 'date: 2022-12-30'
