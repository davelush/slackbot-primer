from flask_restful import Resource
from flask import request


class SlashHandler(Resource):
    def __init__(self, **kwargs):
        self.py_bot = kwargs.get('py_bot')

    def post(self):
        # TODO implement a few slash commands as a test
        slash_text = request.form.get("text")
        response = "This is the slash handler"

        return {"text": response}
