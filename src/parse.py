#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import search

MESSAGE = r"^<@(|[WU].+?)>(.*)"


def valid_message(event):
    return (event["type"] == "message") & ("subtype" not in event)


def split_text(event):
    try:
        text = event["text"]
        results = search(MESSAGE, text)
        return (results.group(1), results.group(2).strip(), event["channel"])
    except AttributeError:
        return (None, None, None)


def messages(events):
    return map(split_text, filter(valid_message, events))


def at_bot(bot_id):
    def f(event):
        user_id, _, _ = event
        return user_id == bot_id

    return f


def remove_user_id(event):
    _, message, channel = event
    return (message, channel)


def parse(bot_id, events):
    return map(remove_user_id, filter(at_bot(bot_id), messages(events)))
