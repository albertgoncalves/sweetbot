#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from re import search
from statistics import mean, median, mode

from scipy.stats import linregress
from numpy import std

from utils import inject, pipe, remove_whitespace, block

NUMERIC = r"[-+]?[0-9]*\.?[0-9]+"
LIST = r"((?:{}\s*,\s*)+{})"
VARIADIC = r"\s*\(\s*{}\s*\)"


def transform_list(command, pattern, f, message):
    try:
        result = \
            pipe( (pattern + VARIADIC).format(inject(LIST, NUMERIC))
                , lambda pattern: search(pattern, command)
                , lambda xs: xs.group(1)
                , eval
                , list
                , f
                , lambda x: round(x, 10)
                , lambda x: "{}".format(x)
                )
        return \
            block("{} = {}".format(remove_whitespace(command), result))
    except:
        return message


def dashboard(command):
    return "Here it is!\nhttp://data-dashboards.sumall.net/sku_metrics/"


def sum_(command):
    return \
        transform_list( command
                      , "sum"
                      , sum
                      , "That didn't work.\nTry `sum(1, 2, 3.01)`"
                      )


def std_(command):
    return \
        transform_list( command
                      , "sd"
                      , std
                      , "No dice!\nTry `sd(-1, 0.01, 1)`"
                      )


def mode_(command):
    return \
        transform_list( command
                      , "mode"
                      , mode
                      , "There may be *no* mode.\nTry `mode(1, 1, 1, 0, 0)`"
                      )


def mean_(command):
    return \
        transform_list( command
                      , "mean"
                      , mean
                      , "I don't understand.\nTry `mean(10, 11, 11.01)`"
                      )


def median_(command):
    return \
        transform_list( command
                      , "median"
                      , median
                      , "Say what?\nTry `median(10, -11, 1000)`"
                      )


def clock(command):
    clock = "%I:%M:%S %p"
    now = datetime.now().strftime(clock)
    now_utc = datetime.utcnow().strftime(clock)
    results = \
        [ "here : {}"
        , "utc  : {}"
        ]
    return block("\n".join(results).format(now, now_utc))


def lm(command):
    try:
        pattern = \
            inject( r"lm\(\s*\[\s*{}\s*\]\s*,\s*\[\s*{}\s*\]\s*\)"
                  , inject(LIST, NUMERIC)
                  )
        xy = search(pattern, command)
        m, b, r, p, _ = \
            linregress(*map(lambda i: list(eval(xy.group(i))), [1, 2]))
        output = \
            [ "{} = ".format(remove_whitespace(command))
            , "    slope     : {:8.4f}"
            , "    intercept : {:8.4f}"
            , "    r-squared : {:8.4f}"
            , "    p-value   : {:8.4f}"
            ]
        return block("\n".join(output).format(m, b, r ** 2, p))
    except:
        return "Wrong way.\nTry `lm([1, 2, 3], [3, 2, 1])`"


def response(command):
    router = \
        { "time": clock
        , "dashboard": dashboard
        , "sum": sum_
        , "mean": mean_
        , "median": median_
        , "mode": mode_
        , "lm": lm
        , "sd": std_
        }
    for key in router.keys():
        if command.startswith(key):
            return router[key](command)
    return "Not sure what you mean."
