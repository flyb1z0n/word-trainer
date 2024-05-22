import json
from openai import OpenAI
from prompts import TRANSLATION_PROMPT
from dataclasses import dataclass


@dataclass
class WordCard:
    text: str
    explanation: str
    transcription: str
    translation: str
    example: str

    def to_message(self) -> str:
        return f"*{self.text}* _(/{self.transcription}/)_ - {self.explanation.lower()} \n\n_Example: {self.example}_"


class LlmService:

    def __init__(self, open_ai_client: OpenAI):
        self.open_ai_client = open_ai_client

    def get_text_card(self, text: str) -> WordCard:
        completion = self.open_ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are assistant that helps users to learn new english words."},
                {"role": "user", "content": TRANSLATION_PROMPT.format(text=str(text))}
            ]
        )
        data = json.loads(str(completion.choices[0].message.content))
        return WordCard(**data)



