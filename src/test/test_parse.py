#!/usr/bin/env python3

from src.parse import at_bot, messages, parse, remove_user_id, split_text, \
    valid_message

BOT_ID = "UXXXXXXXX"
EVENT = \
    { "text": "<@{}> foo bar".format(BOT_ID)
    , "channel": "XXXXXXXXX"
    , "type": "message"
    }
FAIL_TEXT = \
    { "text": "foo bar"
    , "type": EVENT["type"]
    , "channel": EVENT["channel"]
    }
FAIL_TYPE = \
    { "text": EVENT["text"]
    , "type": "baz"
    , "channel": EVENT["channel"]
    }
EVENTS = [EVENT, FAIL_TEXT, FAIL_TYPE]


def test_valid_message():
    assert valid_message({"type": "message", "foo": "bar"})


def test_split_text():
    assert split_text(EVENT) == (BOT_ID, "foo bar", EVENT["channel"])


def test_messages():
    assert list(messages(EVENTS)) == \
        [(BOT_ID, "foo bar", EVENT["channel"]), (None, None, None)]


class TestAtBot(object):
    def test_same_bot(self):
        assert at_bot(BOT_ID)((BOT_ID, None, None))

    def test_different_bots(self):
        assert not at_bot(BOT_ID)(("@that_bot", None, None))


def test_remove_user_id():
    assert remove_user_id(("foo", "bar", "baz")) == ("bar", "baz")


def test_parse():
    assert list(parse(BOT_ID, EVENTS)) == [("foo bar", EVENT["channel"])]
