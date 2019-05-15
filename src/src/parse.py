#!/usr/bin/env python3

from pprint import pprint
from re import search
from typing import Callable, Dict, Iterator, List, Optional, Tuple

THREE_TUPLE = Tuple[Optional[str], Optional[str], Optional[str]]
TWO_TUPLE = Tuple[Optional[str], Optional[str]]
MESSAGE = r"^<@(|[WU].+?)>(.*)"


def valid_message(event: Dict[str, str]) -> bool:
    return (event["type"] == "message") and ("subtype" not in event)


def split_text(event: Dict[str, str]) -> THREE_TUPLE:
    text = event["text"]
    results = search(MESSAGE, text)
    pprint({"text": text})
    if results:
        return (results.group(1), results.group(2).strip(), event["channel"])
    else:
        return (None, None, None)


def at_bot(bot_id: str) -> Callable[[THREE_TUPLE], bool]:
    def f(event):
        (user_id, _, _) = event
        return user_id == bot_id
    return f


def remove_user_id(event: THREE_TUPLE) -> TWO_TUPLE:
    (_, message, channel) = event
    return (message, channel)


def messages(events: List[Dict[str, str]]) -> Iterator[THREE_TUPLE]:
    return map(split_text, filter(valid_message, events))


def parse(bot_id: str, events: List[Dict[str, str]]) -> Iterator[TWO_TUPLE]:
    return map(remove_user_id, filter(at_bot(bot_id), messages(events)))
