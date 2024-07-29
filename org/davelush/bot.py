# -*- coding: utf-8 -*-
import os

from slack_sdk import WebClient


class Bot(object):

    def __init__(self, client: WebClient, client_id: str, client_secret: str):
        super(Bot, self).__init__()
        # self.oauth: dict = {"client_id": client_id,
        #                     "client_secret": client_secret,
        #                     "scope": "bot"}
        self.verification: str = os.environ.get("VERIFICATION_TOKEN")
        self.client: WebClient = client
        self.messages: dict = {}

    # def auth(self, code: int):
    #
    #     auth_response = self.client.api_call(
    #         "oauth.access", auth={}
    #         client_id=self.oauth["client_id"],
    #         client_secret=self.oauth["client_secret"],
    #         code=code
    #     )
    #     team_id = auth_response["team_id"]
    #     authed_teams[team_id] = {"bot_token": auth_response["bot"]["bot_access_token"]}
    #     self.client = WebClient(authed_teams[team_id]["bot_token"])
