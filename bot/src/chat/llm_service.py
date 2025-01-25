import json
from openai import OpenAI

from common.util import timed
from chat.prompts import TRANSLATION_PROMPT
from model.flashcard import Flashcard


class LlmService:

    def __init__(self, open_ai_client: OpenAI):
        self.open_ai_client = open_ai_client

    @timed
    def get_flashcard(self, text: str) -> Flashcard:
        completion = self.open_ai_client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are assistant that helps users to learn new english words."},
                {"role": "user", "content": TRANSLATION_PROMPT.format(text=str(text))}
            ]
        )
        data = json.loads(str(completion.choices[0].message.content))
        return Flashcard(**data)
