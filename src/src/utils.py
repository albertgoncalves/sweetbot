#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any, Callable, Iterator, List, Match, Optional, Union


def block(string: str) -> str:
    return "```{}```".format(string)


def check_float(x: Union[int, float]) -> Union[int, float]:
    int_x = int(x)
    return int_x if int_x == x else x


def extract(match: Optional[Match[str]], i: int) -> Optional[str]:
    return match.group(i) if match else None


def inject(container: str, pattern: Optional[str]) -> str:
    return container.replace("{}", "{pattern}").format(**{"pattern": pattern})


def remove_whitespace(string: str) -> str:
    return string.replace(" ", "")


def newlines(strings: List[str]) -> str:
    return "\n".join(strings)


def pipe(x: Any, *fs: Callable[[Any], Any]) -> Any:
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
    return map(f, string.replace(" ", "").split(",") if string else [])
