import uuid
from typing import Tuple

from dynaconf import settings
from pymongo import MongoClient
from dataclasses import asdict
from llm_service import WordCard

client = MongoClient(settings.DB_URL, settings.DB_PORT)
db = client[settings.DB_NAME]


def _message_collection():
    return db['tg_messages']


def _word_cards():
    return db['word_cards']


def save_message(message):
    _message_collection().insert_one(message)


def save_word_card(user_id: str, word_card: WordCard) -> Tuple[str, WordCard]:
    word_card_entry = asdict(word_card)
    word_card_entry['user_id'] = user_id
    word_card_entry['_id'] = str(uuid.uuid4())
    insert_result = _word_cards().insert_one(word_card_entry)
    return insert_result.inserted_id, word_card


def get_word_card(user_id: str, card_id: str) -> WordCard:
    word_card_dict = _word_cards().find_one({'user_id': user_id, '_id': card_id})
    # Remove the '_id' key from the dictionary
    word_card_dict.pop('_id', None)
    word_card_dict.pop('user_id', None)
    return WordCard(**word_card_dict)
