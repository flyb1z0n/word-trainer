import uuid
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from typing import Tuple

from dynaconf import settings
from pymongo import MongoClient

from chat.util import timed
from model.flashcard import Flashcard


client = MongoClient(settings.DB_URL, settings.DB_PORT)
db = client[settings.DB_NAME]


class ActionDataType(Enum):
    FLASHCARD = 'flashcard'


# The collection that stores the data for messages
def _message_collection():
    return db['tg_messages']


# The collection that stores the data for inline-keyboard actions
def _action_data():
    return db['user_message_action_data']


# The collection that stores the data for flashcards
def _flashcards():
    return db['user_flashcards']


@timed
def save_user_flashcard(user_id: str, flashcard: Flashcard):
    flashcard_entry = dict()
    flashcard_entry['_id'] = str(uuid.uuid4())
    flashcard_entry['created_at'] = datetime.now()
    flashcard_entry['user_id'] = user_id
    flashcard_entry['flashcard'] = asdict(flashcard)
    insert_result = _flashcards().insert_one(flashcard_entry)
    return insert_result.inserted_id


def get_user_flashcards(user_id: str) -> list:
    return list(_flashcards().find({'user_id': user_id}).sort('created_at', -1))

@timed
def delete_user_flashcard(user_id: str, card_id: str):
    _flashcards().delete_one({'user_id': user_id, '_id': card_id})


def save_message(message):
    _message_collection().insert_one(message)

@timed
def save_flashcard_action_data(user_id: str, flashcard: Flashcard, ui_state=None) -> Tuple[str, Flashcard, dict]:
    action_data_entry = dict()
    action_data_entry['user_id'] = user_id
    action_data_entry['_id'] = str(uuid.uuid4())
    action_data_entry['created_at'] = datetime.now()
    action_data_entry['type'] = ActionDataType.FLASHCARD.value
    action_data_entry['data'] = dict()
    action_data_entry['data']['flashcard'] = asdict(flashcard)
    action_data_entry['data']['ui_state'] = ui_state if ui_state is not None else dict()
    insert_result = _action_data().insert_one(action_data_entry)
    return insert_result.inserted_id, flashcard, action_data_entry['data']['ui_state']


@timed
def update_flashcard_action_data_ui_state(user_id: str, card_id: str, ui_state: dict):
    _action_data().update_one({'user_id': user_id, '_id': card_id}, {'$set': {'data.ui_state': ui_state}})


@timed
def get_flashcard_action_data(user_id: str, card_id: str) -> dict:
    action_data_dict = _action_data().find_one({'user_id': user_id, '_id': card_id})
    action_data_dict['data']['flashcard'] = Flashcard(**action_data_dict['data']['flashcard'])
    return action_data_dict
