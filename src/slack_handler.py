from slack_bolt import App
from .openai_service import OpenAIService
import logging

logger = logging.getLogger(__name__)

class SlackHandler:
    def __init__(self, app: App):
        self.app = app
        self.openai_service = OpenAIService()
        self._register_handlers()

    def _register_handlers(self):
        @self.app.message("")
        def handle_message(message, say):
            try:
                # Ignore bot messages and messages without text
                if message.get("subtype") is not None or "text" not in message:
                    return

                text = message["text"]
                source_lang = self.openai_service.detect_language(text)
                target_lang = "russian" if source_lang == "english" else "english"
                
                translation = self.openai_service.translate(text, target_lang)
                response = f"*Original ({source_lang})*:\n{text}\n\n*Translation ({target_lang})*:\n{translation}"
                say(response)
            except Exception as e:
                logger.error(f"Error handling message: {str(e)}")
                say("Sorry, I encountered an error while processing your message.")