""" Test Cases for Helper functions
"""

import pytest
import skdesign.helpers as helpers


def test_is_non_negative():
    """ Test cases for is_non_negative helper """
    with pytest.raises(ValueError):
        helpers.is_non_negative('a', 'Test 1')
    with pytest.raises(ValueError):
        helpers.is_non_negative([1], 'Test 2')
    with pytest.raises(ValueError):
        helpers.is_non_negative(-1, 'Test 3')
    assert helpers.is_non_negative(1, 'Test 4') is None
    assert helpers.is_non_negative(0, 'Test 5') is None


def test_is_positive():
    """ Test cases for is_positive helper """
    with pytest.raises(ValueError):
        helpers.is_positive('a', 'Test 1')
    with pytest.raises(ValueError):
        helpers.is_positive([1], 'Test 2')
    with pytest.raises(ValueError):
        helpers.is_positive(-1, 'Test 3')
    with pytest.raises(ValueError):
        helpers.is_positive(0, 'Test 4')
    assert helpers.is_positive(1, 'Test 5') is None


def test_is_numeric():
    """ Test cases for is_numeric helper """
    with pytest.raises(ValueError):
        helpers.is_numeric('a', 'Test 1')
    with pytest.raises(ValueError):
        helpers.is_numeric([1], 'Test 2')
    assert helpers.is_numeric(-1, 'Test 3') is None
    assert helpers.is_numeric(0, 'Test 4') is None
    assert helpers.is_numeric(1, 'Test 5') is None


def test_is_float():
    """ Test cases for is_float helper """
    with pytest.raises(ValueError):
        helpers.is_float('a', 'Test 1')
    with pytest.raises(ValueError):
        helpers.is_float([1.0], 'Test 2')
    assert helpers.is_float(-1.0, 'Test 3') is None
    assert helpers.is_float(0.0, 'Test 4') is None
    assert helpers.is_float(1.0, 'Test 5') is None
    with pytest.raises(ValueError):
        helpers.is_float(1, 'Test 6')


def test_is_integer():
    """ Test cases for is_integer helper """
    with pytest.raises(ValueError):
        helpers.is_integer('a', 'Test 1')
    with pytest.raises(ValueError):
        helpers.is_integer([1.0], 'Test 2')
    with pytest.raises(ValueError):
        helpers.is_integer(-1.0, 'Test 3')
    with pytest.raises(ValueError):
        helpers.is_integer(0.0, 'Test 4')
    with pytest.raises(ValueError):
        helpers.is_integer(1.0, 'Test 5')
    assert helpers.is_integer(1, 'Test 6') is None
    assert helpers.is_integer(0, 'Test 7') is None
    assert helpers.is_integer(-1, 'Test 8') is None


def test_is_boolean():
    """ Test cases for is_boolean helper """
    with pytest.raises(ValueError):
        helpers.is_boolean('a', 'Test 1')
    with pytest.raises(ValueError):
        helpers.is_boolean([1], 'Test 2')
    with pytest.raises(ValueError):
        helpers.is_boolean(-1, 'Test 3')
    with pytest.raises(ValueError):
        helpers.is_boolean(0, 'Test 4')
    assert helpers.is_boolean(True, 'Test 5') is None
    assert helpers.is_boolean(False, 'Test 6') is None


def test_is_integer_min_2():
    """ Test cases for is_integer_min_2 helper """
    with pytest.raises(ValueError):
        helpers.is_integer_min_2('a', 'Test 1')
    with pytest.raises(ValueError):
        helpers.is_integer_min_2([1.0], 'Test 2')
    with pytest.raises(ValueError):
        helpers.is_integer_min_2(-1.0, 'Test 3')
    with pytest.raises(ValueError):
        helpers.is_integer_min_2(0.0, 'Test 4')
    with pytest.raises(ValueError):
        helpers.is_integer_min_2(1.0, 'Test 5')
    with pytest.raises(ValueError):
        helpers.is_integer_min_2(1, 'Test 6')
    with pytest.raises(ValueError):
        helpers.is_integer_min_2(0, 'Test 7')
    with pytest.raises(ValueError):
        helpers.is_integer_min_2(-1, 'Test 8')
    assert helpers.is_integer_min_2(2, 'Test 9') is None
    assert helpers.is_integer_min_2(100, 'Test 10') is None


def test_is_in_0_1():
    """ Test cases for is_in_0_1 helper """
    with pytest.raises(ValueError):
        helpers.is_in_0_1('a', 'Test 1')
    with pytest.raises(ValueError):
        helpers.is_in_0_1([1.0], 'Test 2')
    with pytest.raises(ValueError):
        helpers.is_in_0_1(-1.0, 'Test 3')
    with pytest.raises(ValueError):
        helpers.is_in_0_1(0.0, 'Test 4')
    with pytest.raises(ValueError):
        helpers.is_in_0_1(1.0, 'Test 5')
    with pytest.raises(ValueError):
        helpers.is_in_0_1(1, 'Test 6')
    with pytest.raises(ValueError):
        helpers.is_in_0_1(-0.1, 'Test 7')
    assert helpers.is_in_0_1(0.1, 'Test 8') is None
