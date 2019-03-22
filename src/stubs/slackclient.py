#!/usr/bin/env python3

from typing import BinaryIO, Dict, List, Optional


class SlackClient(object):
    def __init__(self, token: str) -> None:
        ...

    def api_call( self
                , method: str
                , file: Optional[BinaryIO] = None
                , **kwargs: str
                ) -> Dict[str, str]:
        ...

    def rtm_connect(self, with_team_state: bool, auto_reconnect: bool) -> bool:
        ...

    def rtm_read(self) -> List[Dict[str, str]]:
        ...
