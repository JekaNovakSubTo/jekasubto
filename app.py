import logging
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from src.config import SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET, PORT
from src.slack_handler import SlackHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    try:
        # Initialize Slack app
        slack_app = App(
            token=SLACK_BOT_TOKEN,
            signing_secret=SLACK_SIGNING_SECRET
        )

        # Initialize Slack handler
        SlackHandler(slack_app)

        # Initialize Flask app
        flask_app = Flask(__name__)
        handler = SlackRequestHandler(slack_app)

        @flask_app.route("/slack/events", methods=["POST"])
        def slack_events():
            return handler.handle(request)

        @flask_app.route("/", methods=["GET"])
        def health_check():
            return "Bot is running!"

        return flask_app
    except Exception as e:
        logger.error(f"Error creating app: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        app = create_app()
        app.run(host="0.0.0.0", port=PORT)
    except Exception as e:
        logger.error(f"Failed to start app: {str(e)}")