import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from dotenv import load_dotenv
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def onMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="RESP: " + update.message.text)

def main():
    load_dotenv()
    botToken = os.getenv('TELEGRAM_BOT_TOKEN')
    application = ApplicationBuilder().token(botToken).build()
    
    start_handler = CommandHandler('start', start)
    chat_handler = MessageHandler(None, onMessage)
    application.add_handler(start_handler)
    application.add_handler(chat_handler)
    
    application.run_polling()

if __name__ == '__main__':
    main()