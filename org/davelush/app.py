# -*- coding: utf-8 -*-
import os
import sys
import certifi
from argparse import ArgumentParser, Namespace

import bjoern
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import logging

from slack_sdk import WebClient
from org.davelush.bot import Bot
from org.davelush.logging_setup import setup_loggers, initialise_logging
from org.davelush.handlers.ping_handler import PingHandler
from org.davelush.handlers.event_handler import EventHandler
from org.davelush.handlers.install_handler import InstallHandler
from org.davelush.handlers.post_install_handler import PostInstallHandler
from org.davelush.handlers.slash_handler import SlashHandler


def parse_cli_args(command_line, environment) -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "--client-id",
        action="store_true",
        default=environment.get("CLIENT_ID", "id"),
        help="Client ID for bot authentication"
    )
    parser.add_argument(
        "--client-secret",
        action="store_true",
        default=environment.get("CLIENT_SECRET", "secret"),
        help="Client secret for bot authentication"
    )
    parser.add_argument(
        "--bot-token",
        action="store_true",
        default=environment.get("BOT_TOKEN", "bot_token"),
        help="Token for bot to authenticate back into Slack API"
    )
    arguments: Namespace = parser.parse_args(command_line)

    return arguments


def setup():
    args: Namespace = parse_cli_args(sys.argv[1:], os.environ)
    client: WebClient = WebClient(args.bot_token)
    py_bot: Bot = Bot(client, args.client_id, args.client_secret)

    app: Flask = Flask(__name__)
    CORS(app, resources={'/*': {'origins': '*'}})
    api: Api = Api(app, catch_all_404s=True)
    api.add_resource(EventHandler, '/listening', resource_class_kwargs={'py_bot': py_bot})
    api.add_resource(PostInstallHandler, '/thanks', resource_class_kwargs={'py_bot': py_bot})
    api.add_resource(InstallHandler, '/thanks', resource_class_kwargs={'py_bot': py_bot})
    api.add_resource(SlashHandler, '/slash', resource_class_kwargs={'py_bot': py_bot})
    api.add_resource(PingHandler, '/ping')
    return app, api


setup_loggers()
initialise_logging(logging.INFO)

if __name__ == '__main__':
    flask_app, flask_api = setup()
    logging.info("slack bot start as a bjoern flask app")
    bjoern.run(flask_app, '0.0.0.0', 5000)
