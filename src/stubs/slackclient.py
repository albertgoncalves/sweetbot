#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, List


class SlackClient(object):
    def __init__(self, token: str) -> None:
        ...

    def api_call(self, method: str, **kwargs: str) -> Dict[str, str]:
        ...

    def rtm_connect(self, with_team_state: bool, auto_reconnect: bool) -> bool:
        ...

    def rtm_read(self) -> List[Dict[str, str]]:
        ...
