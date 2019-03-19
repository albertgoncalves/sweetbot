#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import environ
from pprint import pprint
from time import sleep
from typing import Dict, Iterator, Optional, Tuple

from slackclient import SlackClient  # type: ignore

from src.parse import parse
from src.response import response
from src.utils import newlines


def send( slack_client: SlackClient[str]
        , bot_name: Optional[str]
        , command: Optional[str]
        , channel: Optional[str]
        ) -> Dict[str, str]:
    sleep(0.1)
    return slack_client.api_call( "chat.postMessage"
                                , channel=channel
                                , text=response(command, bot_name)
                                )


def loop( slack_client: SlackClient[str]
        , bot_name: Optional[str]
        , commands: Iterator[Tuple[Optional[str], Optional[str]]]
        ) -> None:
    for command in commands:
        pprint(send(slack_client, bot_name, *command))


def death(bot_name: Optional[str]) -> str:
    message = \
        [ "\nNow cracks a noble heart."
        , "Good night {}:"
        , "And flights of angels sing thee to thy rest!"
        ]
    if not bot_name:
        bot_name = "sweet prince"
    return newlines(message).format(bot_name)


def main() -> None:
    bot_name = None
    try:
        slack_client = SlackClient(environ["SLACK_BOT_TOKEN"])
        if slack_client.rtm_connect(with_team_state=False):
            bot_creds = \
                slack_client.api_call("auth.test")
            bot_name = "@{}".format(bot_creds["user"])
            bot_id = bot_creds["user_id"]
            print("Good to see you again, {}.".format(bot_name))
            while True:
                loop( slack_client
                    , bot_name
                    , parse(bot_id, slack_client.rtm_read())
                    )
                sleep(1)
        else:
            print("Hmm, unable to connect.")
    except KeyboardInterrupt:
        print(death(bot_name))


if __name__ == "__main__":
    main()
