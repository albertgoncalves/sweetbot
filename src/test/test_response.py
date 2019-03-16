#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from src.response import clock, eval_list_with, median_, sum_
from src.utils import block, remove_whitespace


class TestEvalListWith(object):
    def head(xs):
        return list(xs)[0]

    pattern = "head"
    command = "{}(1, 2, 3)".format(pattern)
    kwargs = \
        { "f": head
        , "pattern": pattern
        , "message": ["failed"]
        }

    def test_eval(self):
        result = eval_list_with(command=self.command, **self.kwargs)
        response = \
            block("{} = {}".format(self.command.replace(" ", ""), str(1)))
        assert result == response

    def test_fail(self):
        command = "{}(1, 2, a)".format(self.pattern)
        result = eval_list_with(command=command, **self.kwargs)
        assert result == "failed"


def test_sum_():
    command = "sum(1, 2, 3)"
    assert sum_(command) == block("{} = 6".format(remove_whitespace(command)))


class TestMedian(object):
    def test_exact(self):
        command = "median(-11, -10.001, 1000)"
        assert median_(command) == \
            block("{} = -10.001".format(remove_whitespace(command)))

    def test_split(self):
        command = "median(-10.001, -10, 10, 1000)"
        assert median_(command) == \
            block("{} = 0".format(remove_whitespace(command)))


class TestClock(object):
    def test_est(self):
        time = datetime(2019, 1, 1, 0, 0)
        response = block("here : 12:00:00 AM\nutc  : 05:00:00 AM")
        assert clock(time)(None) == response

    def test_edt(self):
        time = datetime(2019, 4, 1, 0, 0)
        response = block("here : 12:00:00 AM\nutc  : 04:00:00 AM")
        assert clock(time)(None) == response
