import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def setup_google_sheets():
    # Define the scope of access
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Load credentials from environment variable
    creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    
    if not creds_json:
        raise ValueError("Google Sheets credentials not found in environment variables.")
    
    creds_dict = json.loads(creds_json)
    
    # Create a credentials object from the JSON dictionary
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
   
   # Authorize and open the Google Sheet by name
   client = gspread.authorize(creds)  
   sheet = client.open("Catatan Keuangan").sheet1  # Replace with your actual sheet name
    
   return sheet

def update_sheet(text):
   sheet = setup_google_sheets()
   sheet.append_row([text])  # Append new row with extracted text 
