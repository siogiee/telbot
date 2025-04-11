import os
import requests
from io import BytesIO
from PIL import Image
import pytesseract 
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Function to set up Google Sheets API access.
def setup_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    # Read credentials from environment variable.
    creds_dict = os.environ.get('GOOGLE_CREDENTIALS')
    
    if creds_dict:
        creds = ServiceAccountCredentials.from_json_keyfile_dict(eval(creds_dict), scope)
        client = gspread.authorize(creds)
        sheet = client.open("Catatan Keuangan").sheet1  # Replace with your actual sheet name
        
        return sheet
    
    raise Exception("Google credentials not found.")

# Function to update Google Sheets with extracted text.
def update_sheet(text):
    sheet = setup_google_sheets()
    sheet.append_row([text])  

# Function to extract text from image using OCR.
def extract_text_from_image(media_url):
    response = requests.get(media_url)
    
    if response.status_code == 200:
        try:
            img = Image.open(BytesIO(response.content))
            text = pytesseract.image_to_string(img)
            return text.strip()  # Return cleaned-up text without extra spaces 
        except Exception as e:
            print(f"Error opening image: {e}")
            return None
    
    print(f"Failed to retrieve image, status code: {response.status_code}")
    return None

# Start command handler function.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Send me a receipt and I'll log it.",
        reply_markup=ForceReply(selective=True),
    )

# Message handler function for handling photo uploads.
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   file_id = update.message.photo[-1].file_id  # Get the highest resolution photo available
   
   new_file = await context.bot.get_file(file_id)  
   media_url = new_file.file_path
   
   text_result = extract_text_from_image(media_url)  
   
   if text_result:  
       update_sheet(text_result)  # Send result to Google Sheets
       await update.message.reply_text(f"Extracted Text:\n{text_result}")
   else:
       await update.message.reply_text("Failed to extract any text.")

if __name__ == '__main__':
   application = ApplicationBuilder().token('8066770324:AAHQBJAvLB95a1jPGZrKjq0mAzVKWMRCO2w').build()  # Replace with your bot token

   application.add_handler(CommandHandler("start", start))
   application.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_photo))

   application.run_polling()
