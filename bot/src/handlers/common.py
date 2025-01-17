import logging
from dynaconf import settings

from chat.db import save_message
from telegram import Update
from telegram.ext import ContextTypes

from chat import messages


def allowed_user_decorator(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message is not None:
            save_message(update.message.to_dict())
        # Only allow messages from the allowed user list
        if str(update.effective_user.id) not in settings.ALLOWED_USERS:
            logging.info("Not allowed user: " + str(update.effective_user.id))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=messages.USER_IS_NOT_IN_ALLOWED_LIST,
                                           parse_mode='Markdown')
            return
        return await func(update, context)

    return wrapper
