import json
import logging

from flask import request, make_response
from flask_restful import Resource

from org.davelush.bot import Bot


def event_handler(event_type, slack_event, py_bot: Bot):
    logging.debug(f"{event_type} and body [{slack_event}]")

    if event_type == "message":
        event = slack_event.get("event")
        message_text = event.get("text")
        if message_text is None and event.get("subtype") != "message_deleted":
            message_text = event.get("message").get("text")
            logging.info("retrieved message_text from event -> message -> text")
        elif event.get("subtype") == "message_deleted":
            logging.info("ignoring a deleted message")
        else:
            logging.info("retrieved message_text from event -> text")
        channel_id = slack_event.get("event").get("channel")
        event_ts = slack_event.get("event").get("ts")
        event_id = slack_event.get("event_id")
        client_msg_id = slack_event.get("event").get("client_msg_id")
        sending_user = f"<@{slack_event.get('event').get('user')}>"

        if message_text is not None:
            logging.info(message_text)
            # TODO this will keep just spamming in a loop
            py_bot.client.chat_postMessage(channel=channel_id, text=f"<Here is a response @{sending_user}>")

        # synchronous acknowledgement response
        message = "Sent response message"
        return make_response(message, 200, )

    elif event_type == "reaction_removed":
        return make_response("Not yet implemented", 200, )
    elif event_type == "emoji_changed":
        return make_response("Not yet implemented", 200, )

    message = "You have not added an event handler for the %s" % event_type
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


def hears(py_bot: Bot):
    slack_event = json.loads(request.data)
    logging.info(slack_event)

    # Verify it's actually Slack sending us events
    if py_bot.verification != slack_event.get("token"):
        message = f"Invalid Slack verification token: {slack_event['token']} pyBot has: {py_bot.verification}"
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    # Handle any events correctly
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event, py_bot)

    # Echo Slack's challenge when you subscribe to events
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    # Canned response for events we're not subscribed to
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids you're looking for.", 404,
                         {"X-Slack-No-Retry": 1})


class EventHandler(Resource):

    def __init__(self, **kwargs):
        self.py_bot = kwargs.get('py_bot')

    def post(self):
        return hears(self.py_bot)

    def get(self):
        return hears(self.py_bot)
