# Slack Bot Primer 🤖

A repository to help get up and running developing a Slack bot quickly

## Pre-requisites
```bash
brew install poetry
brew install ngrok
brew install libev # needed for bjoern
```
- Then go here and create an app https://api.slack.com/apps
- Install it in your workspace and make a note of the OAuth token 
- Sign up for ngrok here https://dashboard.ngrok.com/signup
- Install your authtoken for ngrok here https://dashboard.ngrok.com/get-started/your-authtoken. This is as simple as

```bash
ngrok config add-authtoken <your-ngrok-token-goes-here>
```

## Running the Application

```bash
export $BOT_TOKEN=xoxb-your-slack-oauth-token
poetry run python org/davelush/app.py
```

## Diagnosing Issues

If you get a 
```bash
Failed to send a request to Slack API server: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```
Then follow the solution in https://github.com/slackapi/bolt-python/issues/673

