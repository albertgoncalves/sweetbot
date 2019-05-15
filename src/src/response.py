#!/usr/bin/env python3

from datetime import datetime
from re import search
from statistics import mean, median, mode, stdev
from typing import Any, Callable, Iterator, List, Match, Optional, Tuple

from scipy.stats import linregress
from pytz import utc

from .utils import block, check_float, extract, from_maybe, inject, newlines, \
    pipe, remove_whitespace, spaces, string_to_floats

LIST = r"((?:{}\s*,\s*)+{})"
NUMERIC = r"[-+]?\d*\.?\d+"
VARIADIC = r"\s*\(\s*{}\s*\)"

POST_MESSAGE = "chat.postMessage"
UPLOAD_FILE = "files.upload"


def eval_list_with(
    f: Callable[[Iterator[float]], float],
    command: str,
    pattern: str,
    message: List[str],
    bot_name: Optional[str],
) -> str:
    try:
        result = pipe(
            (pattern + VARIADIC).format(inject(LIST, NUMERIC)),
            lambda pattern: search(pattern, command),
            lambda xs: xs.group(1),
            string_to_floats,
            f,
            lambda x: round(x, 10),
            check_float,
            str,
        )
        return block("{} = {}".format(remove_whitespace(command), result))
    except:
        return newlines(message).format(bot_name)


def sum_(bot_name: Optional[str]) -> Callable[[str], Tuple[str, str]]:
    def f(command):
        message = [
            "That didn't work.",
            "Try `{} sum(1, 2, 3.01)`",
        ]
        return (
            POST_MESSAGE,
            eval_list_with(sum, command, "sum", message, bot_name),
        )
    return f


def mean_(bot_name: Optional[str]) -> Callable[[str], Tuple[str, str]]:
    def f(command):
        message = [
            "I don't understand.",
            "Try `{} mean(10, 11, 11.01)`",
        ]
        return (
            POST_MESSAGE,
            eval_list_with(mean, command, "mean", message, bot_name),
        )
    return f


def median_(bot_name: Optional[str]) -> Callable[[str], Tuple[str, str]]:
    def f(command):
        message = [
            "Say what?",
            "Try `{} median(10, -11, 1000)`",
        ]
        return (
            POST_MESSAGE,
            eval_list_with(median, command, "median", message, bot_name),
        )
    return f


def mode_(bot_name: Optional[str]) -> Callable[[str], Tuple[str, str]]:
    def f(command):
        message = [
            "There may be *no* mode.",
            "Try `{} mode(1, 1, 1, 0, 0)`",
        ]
        return (
            POST_MESSAGE,
            eval_list_with(mode, command, "mode", message, bot_name),
        )
    return f


def sd(bot_name: Optional[str]) -> Callable[[str], Tuple[str, str]]:
    def f(command):
        message = [
            "No dice!",
            "Try `{} sd(-1, 0.01, 1)`",
        ]
        return (
            POST_MESSAGE,
            eval_list_with(stdev, command, "sd", message, bot_name),
        )
    return f


def dashboard(_: Any) -> Tuple[str, str]:
    message = [
        "The three favorite children:",
        "http://data-dashboards.sumall.net/sku_metrics/",
        "http://data-dashboards.sumall.net/adjusted_orders/",
        "http://data-dashboards.sumall.net/bin_viewer/",
    ]
    return (POST_MESSAGE, newlines(message))


def clock(now_here: datetime) -> Callable[[Any], Tuple[str, str]]:
    def f(_):
        timestamp = "%I:%M:%S %p"
        now_utc = now_here.astimezone(utc)
        results = [
            "here : {}",
            "utc  : {}",
        ]
        nows = map(lambda now: now.strftime(timestamp), [now_here, now_utc])
        return (POST_MESSAGE, block(newlines(results).format(*nows)))
    return f


def iter_from_maybe(
    string: Optional[Match[str]]
) -> Callable[[int], List[float]]:
    def f(i):
        return pipe(
            extract(string, i),
            string_to_floats,
            from_maybe,
        )
    return f


def lm(bot_name: Optional[str]) -> Callable[[str], Tuple[str, str]]:
    def f(command):
        try:
            pattern = inject(
                r"lm\(\s*\[\s*{}\s*\]\s*,\s*\[\s*{}\s*\]\s*\)",
                inject(LIST, NUMERIC),
            )
            xy_string = search(pattern, command)
            x, y = map(iter_from_maybe(xy_string), [1, 2])
            m, b, r, p, _ = linregress(x, y)
            output = [
                "{} =".format(remove_whitespace(command)),
                "    slope     : {:8.9f}",
                "    intercept : {:8.9f}",
                "    r-squared : {:8.9f}",
                "    p-value   : {:8.9f}",
            ]
            return (
                POST_MESSAGE,
                block(newlines(output).format(m, b, r ** 2, p)),
            )
        except:
            message = [
                "Wrong way.",
                "Try `{} lm([1, 2, 3], [3, 2, 1])`",
            ]
            return (POST_MESSAGE, newlines(message).format(bot_name))
    return f


def alive(_: Any) -> Tuple[str, str]:
    return (POST_MESSAGE, "I endure amongst the living.")


def dreams(_: Any) -> Tuple[str, str]:
    message = [
        "Had I the heaven's embroidered cloths,",
        "Enwrought with golden and silver light,",
        "The blue and the dim and the dark cloths ",
        "Of night and light and the half-light;",
        "I would spread the cloths under your feet:",
        "But I, being poor, have only my dreams;",
        "I have spread my dreams under your feet;",
        "Tread softly because you tread on my dreams.",
    ]
    return (POST_MESSAGE, newlines(message))


def truth(_: Any) -> Tuple[str, str]:
    message = [
        "The bud disappears in the bursting-forth of the blossom, and one",
        "might say that the former is refuted by the latter; similarly, when",
        "the fruit appears, the blossom is shown up in its turn as a false",
        "manifestation of the plant, and the fruit now emerges as the",
        "*truth* of it instead.",
    ]
    return (POST_MESSAGE, spaces(message))


def hanz_and_franz(_: Any) -> Tuple[str, str]:
    return (UPLOAD_FILE, "imgs/hf.png")


def options(bot_name: Optional[str]) -> Callable[[Any], Tuple[str, str]]:
    def f(_):
        message = [
            "Things you can to do while I'm not dead:",
            " `{} sum(1, 2, 3)`",
            " `{} mean(-100, 0, 101)`",
            " `{} median(-1, 2, 10000)`",
            " `{} mode(1, 1, 1, 1.01)`",
            " `{} sd(-10, 0, 10, 11)`",
            " `{} lm([1, 1, 1, 2], [5, 5, 6, 8])`",
            " `{} time`",
            " `{} dashboard`",
            " `{} alive`",
            " `{} dreams`",
            " `{} truth`",
            " `{} help`",
            " `{} options`",
        ]
        return (POST_MESSAGE, inject(newlines(message), bot_name))
    return f


def response(
    command: Optional[str],
    bot_name: Optional[str],
) -> Tuple[str, str]:
    if command:
        router = {
            "help": options(bot_name),
            "option": options(bot_name),
            "sum": sum_(bot_name),
            "mean": mean_(bot_name),
            "median": median_(bot_name),
            "mode": mode_(bot_name),
            "sd": sd(bot_name),
            "lm": lm(bot_name),
            "dashboard": dashboard,
            "time": clock(datetime.now()),
            "alive": alive,
            "dreams": dreams,
            "truth": truth,
        }
        for key in router.keys():
            if command.startswith(key):
                return router[key](command)
            elif ("hanz" in command) or ("franz" in command):
                return hanz_and_franz(command)
    return \
        (POST_MESSAGE, "I don't know what that means. See what Bernar says.")
