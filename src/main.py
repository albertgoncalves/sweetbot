#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import environ
from time import sleep
from pprint import pprint

from slackclient import SlackClient

from response import response
from parse import parse
from utils import map_, pipe


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
        return "Rest in peace, {}.".format(bot_name)
    else:
        return "The bot no longer lives."


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
