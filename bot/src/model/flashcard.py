from dataclasses import dataclass


@dataclass
class Flashcard:
    text: str
    explanation: str
    transcription: str
    translation: str
    example: str

    def to_message(self) -> str:
        return f"*{self.text}* _(/{self.transcription}/)_ - {self.explanation.lower()} \n\n_Example: {self.example}_"

    def to_message_with_translation(self) -> str:
        return f"*{self.text}* _(/{self.transcription}/)_ - {self.explanation.lower()} \n\n_Example: {self.example}_\n\nTranslation: {self.translation}"
