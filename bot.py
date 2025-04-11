python
import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from google_sheets import update_sheet
from PIL import Image
import pytesseract
import requests
from io import BytesIO

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token bot Telegram Anda
TELEGRAM_TOKEN = '8066770324:AAHQBJAvLB95a1jPGZrKjq0mAzVKWMRCO2w'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Kirimkan struk atau nota Anda!')

def handle_photo(update: Update, context: CallbackContext) -> None:
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('receipt.jpg')

    # Ekstrak teks dari gambar
    text = extract_text_from_image('receipt.jpg')
    
    # Update Google Sheets
    update_sheet(text)

    update.message.reply_text(f'Teks yang diekstrak: {text}')

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()