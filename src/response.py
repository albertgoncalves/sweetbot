#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from re import search
from statistics import mean, median, mode

from scipy.stats import linregress
from numpy import std

from utils import pipe, remove_whitespace

NUMERIC = r"[-+]?[0-9]*\.?[0-9]+"
LIST = r"((?:{}\s*,\s*)+{})"


def three_dashes(string):
    return "```{}```".format(string)


def inject(container, pattern):
    return container.replace("{}", "{pattern}").format(**{"pattern": pattern})


def eval_list(command, pattern):
    return \
        pipe( search(pattern, command)
            , lambda xs: xs.group(1)
            , eval
            , list
            )


def link(command):
    return "Here it is!\nhttp://data-dashboards.sumall.net/sku_metrics/"


def transform_list(command, pattern, func, message):
    try:
        result = \
            pipe( eval_list(command, pattern.format(inject(LIST, NUMERIC)))
                , func
                , lambda x: round(x, 10)
                , lambda x: "{}".format(x)
                )
        return \
            three_dashes("{} = {}".format(remove_whitespace(command), result))
    except:
        return message


def sum_(command):
    return \
        transform_list( command
                      , r"sum\s*\(\s*{}\s*\)"
                      , sum
                      , "That didn't work.\nTry `sum(1, 2, 3.01)`"
                      )


def std_(command):
    return \
        transform_list( command
                      , r"sd\s*\(\s*{}\s*\)"
                      , std
                      , "No dice!\nTry `sd(-1, 0.01, 1)`"
                      )


def mode_(command):
    return \
        transform_list( command
                      , r"mode\s*\(\s*{}\s*\)"
                      , mode
                      , "There may be *no* mode.\nTry `mode(1, 1, 1, 0, 0)`"
                      )


def mean_(command):
    return \
        transform_list( command
                      , r"mean\s*\(\s*{}\s*\)"
                      , mean
                      , "I don't understand.\nTry `mean(10, 11, 11.01)`"
                      )


def median_(command):
    return \
        transform_list( command
                      , r"median\s*\(\s*{}\s*\)"
                      , median
                      , "You can say that again.\nTry `median(10, 11, 1000)`"
                      )


def clock(command):
    clock = "%I:%M:%S %p"
    now = datetime.now().strftime(clock)
    now_utc = datetime.utcnow().strftime(clock)
    results = \
        [ "here : {}"
        , "utc  : {}"
        ]
    return three_dashes("\n".join(results).format(now, now_utc))


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

        return three_dashes("\n".join(output).format(m, b, r ** 2, p))
    except:
        return "Wrong way.\nTry `lm([1, 2, 3], [3, 2, 1])`"


def response(command):
    if command.startswith("sum"):
        return sum_(command)
    elif command.startswith("sd"):
        return std_(command)
    elif command.startswith("mode"):
        return mode_(command)
    elif command.startswith("mean"):
        return mean_(command)
    elif command.startswith("median"):
        return median_(command)
    elif command.startswith("dashboard"):
        return link(command)
    elif command.startswith("time"):
        return clock(command)
    elif command.startswith("lm"):
        return lm(command)
    else:
        return "Not sure what you mean."
