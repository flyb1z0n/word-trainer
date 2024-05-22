from dynaconf import settings
from pymongo import MongoClient


client = MongoClient(settings.DB_URL, settings.DB_PORT)
db = client[settings.DB_NAME]


def _message_collection():
    return db['tg_messages']


def save_message(message):
    _message_collection().insert_one(message)
