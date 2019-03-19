#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Iterator, List, Match, Optional, Union


def block(string: str) -> str:
    return "```{}```".format(string)


def check_float(x: Union[int, float]) -> Union[int, float]:
    int_x = int(x)
    if float(int_x) == x:
        return int_x
    else:
        return x


def extract(match: Optional[Match[str]], i: int) -> Optional[str]:
    if match is None:
        return None
    else:
        return match.group(i)


def inject(container: str, pattern: str) -> str:
    return container.replace("{}", "{pattern}").format(**{"pattern": pattern})


def remove_whitespace(string: str) -> str:
    return string.replace(" ", "")


def newlines(strings: List[str]) -> str:
    return "\n".join(strings)


def pipe(x, *fs):
    for f in fs:
        x = f(x)
    return x


def spaces(strings: List[str]) -> str:
    return " ".join(strings)


def string_to_floats(string: Optional[str]) -> Iterator[Optional[float]]:
    def f(s):
        try:
            return float(s)
        except ValueError:
            return None
    return map(f, string.replace(" ", "").split(","))
