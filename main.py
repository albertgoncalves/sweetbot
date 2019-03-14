#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import environ
from time import sleep
from pprint import pprint
from re import search

from slackclient import SlackClient


def map_(f, xs):
    return list(map(f, xs))


def pipe(x, *fs):
    for f in fs:
        x = f(x)

    return x


def valid_message(event):
    return (event["type"] == "message") & ("subtype" not in event)


def split_text(event):
    pprint(event)
    try:
        text = event["text"]
        matches = search("^<@(|[WU].+?)>(.*)", text)
        return (matches.group(1), matches.group(2).strip(), event["channel"])
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


def sum_(command):
    numeric = "[-+]?[0-9]*\.?[0-9]+"
    pattern = \
        "!sum (\[(?:{numeric},\s*)+{numeric}\])".format(**{"numeric": numeric})
    try:
        return \
            pipe( search(pattern, command)
                , lambda xs: xs.group(1)
                , eval
                , sum
                , lambda x: round(x, 2)
                , lambda x: "*{}*".format(x)
                )
    except:
        return "That didn't work. Try *!sum [1, 2, 3]*."


def response(command):
    headers = {"sum": "!sum"}
    if command.startswith(headers["sum"]):
        return sum_(command)
    else:
        return "Not sure what you mean. Try *{}*.".format(headers["sum"])


def send(slack_client, command, channel):
    sleep(0.1)
    return \
        slack_client.api_call( "chat.postMessage"
                             , channel=channel
                             , text=response(command)
                             )


def loop(slack_client, commands):
    def f(command):
        return \
            pipe( command
                , lambda command: send(slack_client, *command)
                , pprint
                )
    return map_(f, commands)


def death(bot_name):
    if bot_name:
        return "\nRest in peace, {}.".format(bot_name)
    else:
        return "\nThe bot no longer lives."


def main():
    bot_name = None
    try:
        slack_client = SlackClient(environ["SLACK_BOT_TOKEN"])
        if slack_client.rtm_connect(with_team_state=False):
            bot_creds = slack_client.api_call("auth.test")
            bot_name = bot_creds["user"]
            bot_id = bot_creds["user_id"]
            print("{} is alive!".format(bot_name))
            while True:
                loop(slack_client, parse(bot_id, slack_client.rtm_read()))
                sleep(1)
        else:
            print("Unable to connect.")
    except KeyboardInterrupt:
        print(death(bot_name))


if __name__ == "__main__":
    main()
