#!/usr/bin/env python3

from datetime import datetime
from statistics import stdev

from scipy.stats import linregress  # type: ignore

from src.response import clock, eval_list_with, lm, mean_, median_, mode_, \
    response, sum_, sd
from src.utils import block, newlines, remove_whitespace


class TestEvalListWith(object):
    def head(xs):
        return list(xs)[0]

    pattern = "head"
    command = "{}(1, 2, 3)".format(pattern)
    kwargs = \
        { "f": head
        , "pattern": pattern
        , "message": ["failed"]
        , "bot_name": None
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


def test_sum():
    command = "sum(1, 2, 3)"
    assert sum_(None)(command) == \
        block("{} = 6".format(remove_whitespace(command)))


def test_mean():
    command = "mean(100, 100, 100)"
    assert mean_(None)(command) == \
        block("{} = 100".format(remove_whitespace(command)))


class TestMedian(object):
    def test_exact(self):
        command = "median(-11, -10.001, 1000)"
        assert median_(None)(command) == \
            block("{} = -10.001".format(remove_whitespace(command)))

    def test_split(self):
        command = "median(-10.001, -10, 10, 1000)"
        assert median_(None)(command) == \
            block("{} = 0".format(remove_whitespace(command)))


class TestMode(object):
    def test_no_exception(self):
        command = "mode(1.01, 1.01, 1.01, 0, 0)"
        assert mode_(None)(command) == \
            block("{} = 1.01".format(remove_whitespace(command)))

    def test_exception(self):
        message = \
            [ "There may be *no* mode."
            , "Try `{} mode(1, 1, 1, 0, 0)`".format(None)
            ]
        assert mode_(None)("mode(1.01, 1.01, 0, 0)") == newlines(message)


def test_sd():
    a, b, c = -1, 0, 1.01
    x = stdev([a, b, c])
    command = "sd({}, {}, {})".format(a, b, c)
    assert sd(None)(command) == \
        block("{} = {}".format(remove_whitespace(command), round(x, 10)))


def test_lm():
    x = [1, 2, 3]
    y = [4, 5, 100]
    m, b, r, p, _ = linregress(x, y)
    command = "lm({}, {})".format(x, y)
    response = \
        [ "{} =".format(remove_whitespace(command))
        , "    slope     : {:8.9f}"
        , "    intercept : {:8.9f}"
        , "    r-squared : {:8.9f}"
        , "    p-value   : {:8.9f}"
        ]
    assert lm(None)(command) == \
        block(newlines(response).format(m, b, r ** 2, p))


class TestResponse(object):
    def test_fallback(self):
        assert response("", None) == "Sorry, what is it you're trying to say?"

    def test_alive(self):
        assert response("alive", None) == "I endure amongst the living."


class TestClock(object):
    def test_est(self):
        time = datetime(2019, 1, 1, 0, 0)
        response = block("here : 12:00:00 AM\nutc  : 05:00:00 AM")
        assert clock(time)(None) == response

    def test_edt(self):
        time = datetime(2019, 4, 1, 0, 0)
        response = block("here : 12:00:00 AM\nutc  : 04:00:00 AM")
        assert clock(time)(None) == response
