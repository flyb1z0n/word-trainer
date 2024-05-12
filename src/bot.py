import logging

from dynaconf import settings
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from dotenv import load_dotenv
import os
from openai import OpenAI

from src.db import save_message

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

global openAiClient


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only allow messages from the allowed user
    if update.effective_user.id != settings.FlYB1Z0N_USER_ID:
        logging.info("Not allowed user: " + str(update.effective_user.id) + " - " + update.message.text) 
        return

    save_message(update.message.to_dict())
    response = call_open_ai(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(response))


def call_open_ai(text):
    global openAiClient
    prompt="""
    Given text '"""+str(text)+"""', respond with with the following:
    1. Explain in one sentence(using simple english) what does '"""+str(text)+"""' mean?
    2. Provide english transcription.
    3. Translate to russian.
    4. Give an example of using it in a sentence.
    Strictly follow the format, split each response with a new line.
    No further question, just do.
    """

    completion = openAiClient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are assistant that helps users to learn new english words."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


def main():

    global openAiClient
    load_dotenv(override=True)
    botToken = os.getenv('TELEGRAM_BOT_TOKEN')

    openAiClient = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    application = ApplicationBuilder().token(botToken).build()
    
    start_handler = CommandHandler('start', start)
    chat_handler = MessageHandler(None, on_message)
    application.add_handler(start_handler)
    application.add_handler(chat_handler)
    
    application.run_polling()


if __name__ == '__main__':
    main()
