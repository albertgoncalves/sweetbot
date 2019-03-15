#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from os import environ
from time import sleep
from pprint import pprint
from re import search

from scipy.stats import linregress
from numpy import std

from slackclient import SlackClient

NUMERIC = "[-+]?[0-9]*\.?[0-9]+"
LIST = "((?:{}\s*,\s*)+{})"


def map_(f, xs):
    return list(map(f, xs))


def pipe(x, *fs):
    for f in fs:
        x = f(x)

    return x


def inject(container, pattern):
    return container.replace("{}", "{pattern}").format(**{"pattern": pattern})


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


def eval_list(command, pattern):
    return \
        pipe( search(pattern, command)
            , lambda xs: xs.group(1)
            , eval
            , list
            )


def crush(func):
    def f(xs):
        return \
            pipe( xs
                , func
                , lambda x: round(x, 10)
                , lambda x: "{}".format(x)
                )

    return f


def link(command):
    return "Here it is!\nhttp://data-dashboards.sumall.net/sku_metrics/"


def sum_(command):
    try:
        args = (LIST, NUMERIC)
        return \
            pipe( eval_list(command, "sum\s*\(\s{}\s\)".format(inject(*args)))
                , crush(sum)
                )
    except:
        return "That didn't work.\nTry `sum(1, 2, 3.01)`"


def sd(command):
    try:
        args = (LIST, NUMERIC)
        return \
            pipe( eval_list(command, "sd\s*\(\s{}\s\)".format(inject(*args)))
                , crush(std)
                )
    except:
        return "No dice!\nTry `sd(-1, 0.01, 1)`"


def now(command):
    utcnow = datetime.utcnow().strftime("%I:%M:%S %p")
    return "Current time UTC\n`{}`".format(utcnow)


def lm(command):
    try:
        pattern = \
            inject( "lm\(\s*\[\s*{}\s*\]\s*,\s*\[\s*{}\s*\]\s*\)"
                  , inject(LIST, NUMERIC)
                  )

        xy = search(pattern, command)
        m, b, r, p, _ = \
            linregress(*map(lambda i: list(eval(xy.group(i))), [1, 2]))

        output = \
            [ "slope: {}"
            , "intercept: {}"
            , "r-squared: {}"
            , "p-value: {}"
            ]

        return "\n".join(output).format(m, b, r ** 2, p)
    except:
        return "Wrong way.\nTry `lm([1, 2, 3], [3, 2, 1])`"


def response(command):
    if command.startswith("sum"):
        return sum_(command)
    elif command.startswith("sd"):
        return sd(command)
    elif command.startswith("dashboard"):
        return link(command)
    elif command.startswith("utc"):
        return now(command)
    elif command.startswith("lm"):
        return lm(command)
    else:
        return "Not sure what you mean."


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
