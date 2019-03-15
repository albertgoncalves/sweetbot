#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def map_(f, xs):
    return list(map(f, xs))


def pipe(x, *fs):
    for f in fs:
        x = f(x)

    return x


def remove_whitespace(command):
    return command.replace(" ", "")


def block(string):
    return "```{}```".format(string)


def inject(container, pattern):
    return container.replace("{}", "{pattern}").format(**{"pattern": pattern})
