import uuid
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from typing import Tuple

from dynaconf import settings
from pymongo import MongoClient

from model.flashcard import Flashcard

client = MongoClient(settings.DB_URL, settings.DB_PORT)
db = client[settings.DB_NAME]


class ActionDataType(Enum):
    FLASHCARD = 'flashcard'


def _message_collection():
    return db['tg_messages']


def _action_data():
    return db['user_message_action_data']


def save_message(message):
    _message_collection().insert_one(message)


def save_flashcard_action_data(user_id: str, flashcard: Flashcard) -> Tuple[str, Flashcard]:
    action_data_entry = dict()
    action_data_entry['user_id'] = user_id
    action_data_entry['_id'] = str(uuid.uuid4())
    action_data_entry['created_at'] = datetime.now()
    action_data_entry['type'] = ActionDataType.FLASHCARD.value
    action_data_entry['data'] = asdict(flashcard)
    insert_result = _action_data().insert_one(action_data_entry)
    return insert_result.inserted_id, flashcard


def get_flashcard_action_data(user_id: str, card_id: str) -> Flashcard:
    flashcard_dict = _action_data().find_one({'user_id': user_id, '_id': card_id})
    return Flashcard(**flashcard_dict['data'])
