import logging
import os
from enum import Enum

from dotenv import load_dotenv
from dynaconf import settings
from openai import OpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from db import (save_message, save_flashcard_action_data, get_flashcard_action_data,
                update_flashcard_action_data_ui_state, save_user_flashcard, delete_user_flashcard, get_user_flashcards)
from llm_service import LlmService
from model.flashcard import Flashcard

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

global llm_service


class Actions(Enum):
    REFRESH = 'refresh'
    TRANSLATE = 'translate'
    SAVE = 'save'
    REMOVE = 'remove'

    def cb_data(self, card_id: str) -> str:
        return f"{self.value} {card_id}"

    def pattern(self):
        return f"^{self.value} .*"


class Commands(Enum):
    START = 'start'
    DICTIONARY = 'dictionary'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def show_dictionary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    saved_flashcards = get_user_flashcards(user_id)
    if not saved_flashcards:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You don't have any saved flashcards.")
        return

    message = "Last 10 saved words:\n\n"
    for idx, entry in enumerate(saved_flashcards[:10]):
        flashcard = Flashcard(**entry['flashcard'])
        message += str(idx + 1) + ". " + flashcard.text + "\n\n"

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   parse_mode='Markdown',
                                   text=message)


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_message(update.message.to_dict())
    # Only allow messages from the allowed user
    if update.effective_user.id != settings.FlYB1Z0N_USER_ID and update.effective_user.id != settings.JANE_USER_ID:
        logging.info("Not allowed user: " + str(update.effective_user.id) + " - " + update.message.text)
        return

    text = update.message.text
    # TODO: add validation for the text size.
    response = llm_service.get_flashcard(text)
    card_id, _, ui_state = save_flashcard_action_data(str(update.effective_user.id), response)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=response.to_message(ui_state),
                                   parse_mode='Markdown',
                                   reply_markup=build_keyboard(card_id, ui_state)
                                   )


async def on_refresh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    prev_card_id = update.callback_query.data.split(" ")[1]
    action_data = get_flashcard_action_data(str(update.effective_user.id), prev_card_id)
    text = action_data['data']['flashcard'].text
    response = llm_service.get_flashcard(text)
    card_id, _, ui_state = save_flashcard_action_data(str(update.effective_user.id), response,
                                                      action_data['data']['ui_state'])

    await query.edit_message_text(
        text=response.to_message(ui_state),
        parse_mode='Markdown',
        reply_markup=build_keyboard(card_id, ui_state)
    )


async def on_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    card_id = update.callback_query.data.split(" ")[1]
    action_data = get_flashcard_action_data(str(update.effective_user.id), card_id)
    flashcard = action_data['data']['flashcard']
    ui_state = action_data['data']['ui_state']
    ui_state['translation_shown'] = True
    update_flashcard_action_data_ui_state(str(update.effective_user.id), card_id, ui_state)
    await query.edit_message_text(
        text=flashcard.to_message(ui_state),
        parse_mode='Markdown',
        reply_markup=build_keyboard(card_id, ui_state)
    )


async def on_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    card_id = update.callback_query.data.split(" ")[1]
    action_data = get_flashcard_action_data(str(update.effective_user.id), card_id)
    flashcard = action_data['data']['flashcard']
    ui_state = action_data['data']['ui_state']
    # TODO add validation (size,
    flashcard_id = save_user_flashcard(str(update.effective_user.id), flashcard)
    ui_state['saved_flash_card_id'] = flashcard_id
    update_flashcard_action_data_ui_state(str(update.effective_user.id), card_id, ui_state)
    await query.edit_message_text(
        text=flashcard.to_message(ui_state),
        parse_mode='Markdown',
        reply_markup=build_keyboard(card_id, ui_state)
    )


async def on_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    card_id = update.callback_query.data.split(" ")[1]
    action_data = get_flashcard_action_data(str(update.effective_user.id), card_id)
    flashcard = action_data['data']['flashcard']
    ui_state = action_data['data']['ui_state']
    flashcard_id = ui_state.get('saved_flash_card_id', None)
    if flashcard_id is not None:
        delete_user_flashcard(str(update.effective_user.id), flashcard_id)
    ui_state['saved_flash_card_id'] = None
    update_flashcard_action_data_ui_state(str(update.effective_user.id), card_id, ui_state)
    await query.edit_message_text(
        text=flashcard.to_message(ui_state),
        parse_mode='Markdown',
        reply_markup=build_keyboard(card_id, ui_state)
    )


def build_keyboard(card_id: str, ui_state: dict):
    # Emoji Unicode: https://www.iemoji.com/
    buttons = []
    is_saved = ui_state.get('saved_flash_card_id', None) is not None

    if not is_saved:
        buttons.append(InlineKeyboardButton("\U0001F504 Refresh", callback_data=Actions.REFRESH.cb_data(card_id)))

    if not ui_state.get('translation_shown', False):
        buttons.append(InlineKeyboardButton("\U0001F4D6 Translate", callback_data=Actions.TRANSLATE.cb_data(card_id)))

    if is_saved:
        buttons.append(InlineKeyboardButton("\U0001F5D1 Remove", callback_data=Actions.REMOVE.cb_data(card_id)))
    else:
        buttons.append(InlineKeyboardButton("\U0001F4BE Add", callback_data=Actions.SAVE.cb_data(card_id)))

    return InlineKeyboardMarkup([buttons])


def main():
    global llm_service
    load_dotenv(override=True)
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

    open_ai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    llm_service = LlmService(open_ai_client)
    application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler(Commands.START.value, start)
    saved_cards_handler = CommandHandler(Commands.DICTIONARY.value, show_dictionary)
    chat_handler = MessageHandler(filters.TEXT, on_message)
    application.add_handler(start_handler)
    application.add_handler(saved_cards_handler)
    application.add_handler(chat_handler)
    application.add_handler(CallbackQueryHandler(on_refresh, Actions.REFRESH.pattern()))
    application.add_handler(CallbackQueryHandler(on_translate, Actions.TRANSLATE.pattern()))
    application.add_handler(CallbackQueryHandler(on_save, Actions.SAVE.pattern()))
    application.add_handler(CallbackQueryHandler(on_remove, Actions.REMOVE.pattern()))
    application.run_polling()


if __name__ == '__main__':
    main()
