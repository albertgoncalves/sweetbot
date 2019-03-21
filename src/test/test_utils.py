#!/usr/bin/env python3

from src.utils import check_float, inject, pipe, string_to_floats


class TestCheckFloat(object):
    def test_is_int(self):
        assert check_float(4.0) == 4

    def test_is_float(self):
        assert check_float(4.1) == 4.1


class TestInject(object):
    def test_two(self):
        assert inject("{}{}", "foobar") == "foobarfoobar"

    def test_zero(self):
        assert inject("foo", "bar") == "foo"


def test_pipe():
    x = 10.5
    y = 2
    assert pipe(x, int, float, lambda x: x / y) == (float(int(x))) / y


def test_string_to_floats():
    assert list(string_to_floats("-1, 0.001, 1.0")) == [-1.0, 0.001, 1.0]
