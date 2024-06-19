from dataclasses import dataclass


@dataclass
class Flashcard:
    text: str
    explanation: str
    transcription: str
    translation: str
    example: str

    def to_message(self, ui_state: dict = None) -> str:
        if ui_state is None:
            ui_state = dict()
        message = f"*{self.text}* _(/{self.transcription}/)_ - {self.explanation.lower()} \n\n_Example: {self.example}_"
        if ui_state.get('translation_shown', False):
            message += f"\n\nTranslation: {self.translation}"
        return message
