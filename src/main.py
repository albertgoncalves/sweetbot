#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import environ
from time import sleep
from pprint import pformat

from slackclient import SlackClient

from response import response
from parse import parse
from utils import map_, newlines, pipe


def send(slack_client):
    def f(packet):
        command, channel = packet
        sleep(0.1)
        return slack_client.api_call( "chat.postMessage"
                                    , channel=channel
                                    , text=response(command)
                                    )
    return f


def loop(slack_client, commands):
    def f(packet):
        return \
            pipe( packet
                , send(slack_client)
                , pformat
                , print
                )
    return map_(f, commands)


def death(bot_name):
    message = \
        [ "\nNow cracks a noble heart."
        , "Good night {}:"
        , "And flights of angels sing thee to thy rest!"
        ]
    if not bot_name:
        bot_name = "sweet prince"
    return newlines(message).format(bot_name)


def main():
    bot_name = None
    try:
        slack_client = SlackClient(environ["SLACK_BOT_TOKEN"])
        if slack_client.rtm_connect(with_team_state=False):
            bot_creds = slack_client.api_call("auth.test")
            bot_name = bot_creds["user"]
            bot_id = bot_creds["user_id"]
            print("Good to see you again, {}.".format(bot_name))
            while True:
                loop(slack_client, parse(bot_id, slack_client.rtm_read()))
                sleep(1)
        else:
            print("Hmm, unable to connect.")
    except KeyboardInterrupt:
        print(death(bot_name))


if __name__ == "__main__":
    main()
