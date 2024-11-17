
import openai
from typing import Literal
from .config import OPENAI_API_KEY

LanguageType = Literal["russian", "english"]

class OpenAIService:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.model = "text-davinci-003"

    def _get_completion(self, prompt: str) -> str:
        try:
            response = openai.Completion.create(
                engine=self.model,
                prompt=prompt,
                max_tokens=1000,
                temperature=0.7,
                n=1,
                stop=None
            )
            return response.choices[0].text.strip()
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API Error: {str(e)}")
            return f"Error from OpenAI API: {str(e)}"
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return f"Unexpected error: {str(e)}"

    def detect_language(self, text: str) -> LanguageType:
        if not text.strip():
            logging.warning("Empty text provided for language detection.")
            return "english"  # Default to English if input is empty
        prompt = f"Determine if this text is Russian or English: {text}"
        response = self._get_completion(prompt).lower()
        if "русск" in response or "russian" in response:
            return "russian"
        return "english"

    def translate(self, text: str, target_lang: LanguageType) -> str:
        if not text.strip():
            logging.warning("Empty text provided for translation.")
            return "No text provided for translation."
        prompt = (
            f"Переведи этот текст на {target_lang}: {text}" if target_lang == "russian"
            else f"Translate this text to {target_lang}: {text}"
        )
        return self._get_completion(prompt)
