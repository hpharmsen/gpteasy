import pytest
from justdays import Day

def test_add_int():
    assert Day('2022-12-30') + 3 == Day(2023,1,2)

def test_add_int_right():
    assert 3 + Day('2022-12-30') == Day(2023,1,2)

def test_add_str():
    assert Day('2022-12-30') + ' is the day' == '2022-12-30 is the day'

def test_add_str_right():
    assert 'date: ' + Day('2022-12-30') == 'date: 2022-12-30'

def test_add_float():
    with pytest.raises(TypeError):
        Day() + 1.0

def test_substract_day():
    assert Day('2023-01-02') - Day('2022-12-30') == 3

def test_substract_int():
    assert Day('2023-01-02') - 3 == Day('2022-12-30')

def test_substract_float():
    with pytest.raises(TypeError):
        Day() - 1.0
