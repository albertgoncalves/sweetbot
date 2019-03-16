#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.utils import check_float, inject, map_, pipe, string_to_floats


class TestCheckFloat(object):
    def test_is_int(self):
        assert check_float(4.0) == 4

    def test_is_float(self):
        assert check_float(4.1) == 4.1


def test_inject():
    assert inject("{}{}", "foobar") == "foobarfoobar"
    assert inject("foo", "bar") == "foo"


def test_map_():
    assert map_(lambda x: x + 10, range(5)) == [10, 11, 12, 13, 14]


def test_pipe():
    assert pipe(1.5, int, float, type) == type(float(int(1.5)))


def test_string_to_floats():
    assert list(string_to_floats("-1, 0.001, 1.0")) == [-1.0, 0.001, 1.0]
