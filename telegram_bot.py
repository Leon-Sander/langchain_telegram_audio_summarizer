from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, CallbackContext
from audio_summarizer import AudioSummarizer
from dotenv import load_dotenv
from telegram import Update
import tempfile  
import logging
import os
load_dotenv()

audio_summarizer = AudioSummarizer()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a Voice to Text transcriber and summary bot, please send voice messages and audio files!")

async def handle_file(file, update: Update, context: CallbackContext):
    with tempfile.NamedTemporaryFile(suffix=".ogg") as temp_file:
        await file.download_to_drive(temp_file.name)
        output_dict = audio_summarizer.summarize()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="TRANSCRIBED TEXT: " + output_dict["full_text"])
        await context.bot.send_message(chat_id=update.effective_chat.id, text="SUMMARY: " + output_dict["summary"])

def check_user_id(update: Update):
    if update.effective_chat.id == int(os.getenv("USER_ID")):
        return True
    else:
        return False

async def handle_voice_message(update: Update, context: CallbackContext):
    if check_user_id(update):
        file = await update.message.voice.get_file()
        await handle_file(file, update, context)

async def handle_audio_message(update: Update, context: CallbackContext):
    if check_user_id(update):
        file = await update.message.audio.get_file()
        await handle_file(file, update, context)

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    start_handler = CommandHandler('start', start)
    voice_handler = MessageHandler(filters.VOICE & (~filters.COMMAND), handle_voice_message)
    audio_handler = MessageHandler(filters.AUDIO & (~filters.COMMAND), handle_audio_message)
    application.add_handler(start_handler)
    application.add_handler(voice_handler)
    application.add_handler(audio_handler)
    application.run_polling()