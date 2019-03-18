#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from re import search
from statistics import mean, median, mode, stdev

from scipy.stats import linregress
from pytz import utc

from .utils import block, check_float, inject, newlines, pipe, \
    remove_whitespace, spaces, string_to_floats

BOT_NAME = "@sweetbot"
LIST = r"((?:{}\s*,\s*)+{})"
NUMERIC = r"[-+]?\d*\.?\d+"
VARIADIC = r"\s*\(\s*{}\s*\)"


def eval_list_with(f, command, pattern, message):
    try:
        result = \
            pipe( (pattern + VARIADIC).format(inject(LIST, NUMERIC))
                , lambda pattern: search(pattern, command)
                , lambda xs: xs.group(1)
                , string_to_floats
                , f
                , lambda x: round(x, 10)
                , check_float
                , str
                )
        return \
            block("{} = {}".format(remove_whitespace(command), result))
    except:
        return newlines(message).format(BOT_NAME)


def sum_(command):
    message = \
        [ "That didn't work."
        , "Try `{} sum(1, 2, 3.01)`"
        ]
    return eval_list_with(sum, command, "sum", message)


def mean_(command):
    message = \
        [ "I don't understand."
        , "Try `{} mean(10, 11, 11.01)`"
        ]
    return eval_list_with(mean, command, "mean", message)


def median_(command):
    message = \
        [ "Say what?"
        , "Try `{} median(10, -11, 1000)`"
        ]
    return eval_list_with(median, command, "median", message)


def mode_(command):
    message = \
        [ "There may be *no* mode."
        , "Try `{} mode(1, 1, 1, 0, 0)`"
        ]
    return eval_list_with(mode, command, "mode", message)


def sd(command):
    message = \
        [ "No dice!"
        , "Try `{} sd(-1, 0.01, 1)`"
        ]
    return eval_list_with(stdev, command, "sd", message)


def dashboard(_):
    message = \
        [ "The three favorite children:"
        , "http://data-dashboards.sumall.net/sku_metrics/"
        , "http://data-dashboards.sumall.net/adjusted_orders/"
        , "http://data-dashboards.sumall.net/bin_viewer/"
        ]
    return newlines(message)


def clock(now_here):
    def f(_):
        timestamp = "%I:%M:%S %p"
        now_utc = now_here.astimezone(utc)
        results = \
            [ "here : {}"
            , "utc  : {}"
            ]
        nows = map(lambda now: now.strftime(timestamp), [now_here, now_utc])
        return block(newlines(results).format(*nows))
    return f


def lm(command):
    try:
        pattern = \
            inject( r"lm\(\s*\[\s*{}\s*\]\s*,\s*\[\s*{}\s*\]\s*\)"
                  , inject(LIST, NUMERIC)
                  )
        xy = search(pattern, command)
        m, b, r, p, _ = \
            linregress(*map( lambda i: list(string_to_floats(xy.group(i)))
                           , [1, 2]
                           ))
        output = \
            [ "{} =".format(remove_whitespace(command))
            , "    slope     : {:8.9f}"
            , "    intercept : {:8.9f}"
            , "    r-squared : {:8.9f}"
            , "    p-value   : {:8.9f}"
            ]
        return block(newlines(output).format(m, b, r ** 2, p))
    except:
        return "Wrong way.\nTry `{} lm([1, 2, 3], [3, 2, 1])`".format(BOT_NAME)


def alive(_):
    return "I endure amongst the living."


def dreams(_):
    message = \
        [ "Had I the heaven's embroidered cloths,"
        , "Enwrought with golden and silver light,"
        , "The blue and the dim and the dark cloths "
        , "Of night and light and the half-light;"
        , "I would spread the cloths under your feet:"
        , "But I, being poor, have only my dreams;"
        , "I have spread my dreams under your feet;"
        , "Tread softly because you tread on my dreams."
        ]
    return newlines(message)


def truth(_):
    message = \
        [ "The bud disappears in the bursting-forth of the blossom, and one"
        , "might say that the former is refuted by the latter; similarly, when"
        , "the fruit appears, the blossom is shown up in its turn as a false"
        , "manifestation of the plant, and the fruit now emerges as the"
        , "*truth* of it instead."
        ]
    return spaces(message)


def pets(_):
    message = \
        [ "Do I have pets? Sadly, not at the moment. I don't really have space"
        , "for them in my apartment, but I one day I'd like to have an"
        , "*electric sheep*."
        ]
    return spaces(message)


def options(_):
    message = \
        [ "Things you can to do while I'm not dead:"
        , " `{} sum(1, 2, 3)`"
        , " `{} mean(-100, 0, 101)`"
        , " `{} median(-1, 2, 10000)`"
        , " `{} mode(1, 1, 1, 1.01)`"
        , " `{} sd(-10, 0, 10, 11)`"
        , " `{} lm([1, 1, 1, 2], [5, 5, 6, 8])`"
        , " `{} time`"
        , " `{} dashboard`"
        , " `{} alive`"
        , " `{} dreams`"
        , " `{} truth`"
        , " `{} pets`"
        , " `{} help`"
        , " `{} options`"
        ]
    return inject(newlines(message), BOT_NAME)


def response(command):
    router = \
        { "sum": sum_
        , "mean": mean_
        , "median": median_
        , "mode": mode_
        , "sd": sd
        , "dashboard": dashboard
        , "time": clock(datetime.now())
        , "lm": lm
        , "alive": alive
        , "dreams": dreams
        , "truth": truth
        , "pets": pets
        , "help": options
        , "options": options
        }
    for key in router.keys():
        if command.startswith(key):
            return router[key](command)
    return "Sorry, what is it you're trying to say?"
