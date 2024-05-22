import logging
import os

from dotenv import load_dotenv
from dynaconf import settings
from openai import OpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler

from db import save_message
from llm_service import LlmService

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

global llm_service


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only allow messages from the allowed user
    if update.effective_user.id != settings.FlYB1Z0N_USER_ID and update.effective_user.id != settings.JANE_USER_ID:
        logging.info("Not allowed user: " + str(update.effective_user.id) + " - " + update.message.text)
        return

    save_message(update.message.to_dict())
    text = update.message.text
    response = llm_service.get_text_card(text)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=response.to_message(),
                                   parse_mode='Markdown',
                                   reply_markup=build_keyboard(text)
                                   )


async def on_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = update.callback_query.data.split(" ")[1]
    response = llm_service.get_text_card(text)
    reply_markup = build_keyboard(text)
    await query.edit_message_text(
        text=response.to_message(),
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


def build_keyboard(text):
    keyboard = [
        [
            InlineKeyboardButton("Refresh", callback_data=str("refresh " + text)),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def main():
    global llm_service
    load_dotenv(override=True)
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

    open_ai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    llm_service = LlmService(open_ai_client)
    application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler('start', start)
    chat_handler = MessageHandler(None, on_message)
    refresh_handler = CallbackQueryHandler(on_callback_query, "^refresh .*")

    application.add_handler(start_handler)
    application.add_handler(chat_handler)
    application.add_handler(refresh_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
