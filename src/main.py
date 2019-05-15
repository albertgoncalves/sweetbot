#!/usr/bin/env python3

from os import environ
from os.path import exists
from pprint import pprint
from time import sleep
from typing import Dict, Iterator, Optional, Tuple

from slackclient import SlackClient

from src.parse import parse
from src.response import POST_MESSAGE, UPLOAD_FILE, response
from src.utils import newlines


class ApiError(Exception):
    pass


def send(
    slack_client: SlackClient,
    bot_name: Optional[str],
    command: Optional[str],
    channel: Optional[str],
) -> Dict[str, str]:
    if command and channel:
        request, payload = response(command, bot_name)
        if request == UPLOAD_FILE:
            if exists(payload):
                with open(payload, "rb") as f:
                    return slack_client.api_call(
                        request,
                        channels=channel,
                        file=f,
                    )
            else:
                request, payload = (POST_MESSAGE, "Hmm... what?")
        return slack_client.api_call(
            request,
            channel=channel,
            text=payload,
        )
    else:
        raise ApiError("Missing channel or command, closing connection.")


def loop(
    slack_client: SlackClient,
    bot_name: Optional[str],
    commands: Iterator[Tuple[Optional[str], Optional[str]]],
) -> None:
    for command in commands:
        response = send(slack_client, bot_name, *command)
        pprint(response)
        ok = response["ok"]
        if ok:
            sleep(0.15)
        else:
            message = \
                "API response returned {}, closing connection.".format(ok)
            raise ApiError(message)


def death(bot_name: Optional[str], exception: str) -> str:
    message = [
        exception,
        "\nNow cracks a noble heart.",
        "Good night {}:",
        "And flights of angels sing thee to thy rest!",
    ]
    if not bot_name:
        bot_name = "sweet prince"
    return newlines(message).format(bot_name)


def main() -> None:
    bot_name = None
    slack_client = SlackClient(environ["SLACK_BOT_TOKEN"])
    kwargs = {"with_team_state": False, "auto_reconnect": True}
    try:
        if slack_client.rtm_connect(**kwargs):
            bot_creds = \
                slack_client.api_call("auth.test")
            bot_name = "@{}".format(bot_creds["user"])
            bot_id = bot_creds["user_id"]
            print("Good to see you again, {}.\n".format(bot_name))
            while True:
                loop(
                    slack_client,
                    bot_name,
                    parse(bot_id, slack_client.rtm_read()),
                )
                sleep(0.75)
        else:
            print("Hmm, unable to connect.")
    except (KeyboardInterrupt, ApiError) as e:
        print(death(bot_name, str(e)))


if __name__ == "__main__":
    main()
