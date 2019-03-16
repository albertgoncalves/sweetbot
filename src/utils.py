#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def block(string):
    return "```{}```".format(string)


def check_float(x):
    int_x = int(x)
    if float(int_x) == x:
        return int_x
    else:
        return x


def inject(container, pattern):
    return container.replace("{}", "{pattern}").format(**{"pattern": pattern})


def map_(f, xs):
    return list(map(f, xs))


def remove_whitespace(string):
    return string.replace(" ", "")


def newlines(strings):
    return "\n".join(strings)


def pipe(x, *fs):
    for f in fs:
        x = f(x)
    return x


def spaces(strings):
    return " ".join(strings)


def string_to_floats(string):
    return map(float, string.replace(",", "").split())
