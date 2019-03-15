#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from os import environ
from time import sleep
from pprint import pprint
from re import search
from statistics import mean, median, mode

from scipy.stats import linregress
from numpy import std

from slackclient import SlackClient

NUMERIC = r"[-+]?[0-9]*\.?[0-9]+"
LIST = r"((?:{}\s*,\s*)+{})"


def map_(f, xs):
    return list(map(f, xs))


def pipe(x, *fs):
    for f in fs:
        x = f(x)

    return x


def three_dashes(string):
    return "```{}```".format(string)


def inject(container, pattern):
    return container.replace("{}", "{pattern}").format(**{"pattern": pattern})


def valid_message(event):
    return (event["type"] == "message") & ("subtype" not in event)


def split_text(event):
    pprint(event)
    try:
        text = event["text"]
        matches = search(r"^<@(|[WU].+?)>(.*)", text)
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


def link(command):
    return "Here it is!\nhttp://data-dashboards.sumall.net/sku_metrics/"


def shrink(command):
    return command.replace(" ", "")


def transform_list(command, pattern, func, message):
    try:
        result = \
            pipe( eval_list(command, pattern.format(inject(LIST, NUMERIC)))
                , func
                , lambda x: round(x, 10)
                , lambda x: "{}".format(x)
                )
        return three_dashes("{} = {}".format(shrink(command), result))
    except:
        return message


def sum_(command):
    return \
        transform_list( command
                      , r"sum\s*\(\s*{}\s*\)"
                      , sum
                      , "That didn't work.\nTry `sum(1, 2, 3.01)`"
                      )


def std_(command):
    return \
        transform_list( command
                      , r"sd\s*\(\s*{}\s*\)"
                      , std
                      , "No dice!\nTry `sd(-1, 0.01, 1)`"
                      )


def mode_(command):
    return \
        transform_list( command
                      , r"mode\s*\(\s*{}\s*\)"
                      , mode
                      , "There may be *no* mode.\nTry `mode(1, 1, 1, 0, 0)`"
                      )


def mean_(command):
    return \
        transform_list( command
                      , r"mean\s*\(\s*{}\s*\)"
                      , mean
                      , "I don't understand.\nTry `mean(10, 11, 11.01)`"
                      )


def median_(command):
    return \
        transform_list( command
                      , r"median\s*\(\s*{}\s*\)"
                      , median
                      , "You can say that again.\nTry `median(10, 11, 1000)`"
                      )


def now(command):
    utcnow = datetime.utcnow().strftime("%I:%M:%S %p")
    return "Current time UTC\n`{}`".format(utcnow)


def lm(command):
    try:
        pattern = \
            inject( r"lm\(\s*\[\s*{}\s*\]\s*,\s*\[\s*{}\s*\]\s*\)"
                  , inject(LIST, NUMERIC)
                  )

        xy = search(pattern, command)
        m, b, r, p, _ = \
            linregress(*map(lambda i: list(eval(xy.group(i))), [1, 2]))

        output = \
            [ "{} = ".format(shrink(command))
            , "    slope     : {:8.4f}"
            , "    intercept : {:8.4f}"
            , "    r-squared : {:8.4f}"
            , "    p-value   : {:8.4f}"
            ]

        return three_dashes("\n".join(output).format(m, b, r ** 2, p))
    except:
        return "Wrong way.\nTry `lm([1, 2, 3], [3, 2, 1])`"


def response(command):
    if command.startswith("sum"):
        return sum_(command)
    elif command.startswith("sd"):
        return std_(command)
    elif command.startswith("mode"):
        return mode_(command)
    elif command.startswith("mean"):
        return mean_(command)
    elif command.startswith("median"):
        return median_(command)
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
