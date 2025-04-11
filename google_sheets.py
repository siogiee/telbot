python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def setup_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Catatan Keuangan").sheet1
    
    return sheet

def update_sheet(text):
    sheet = setup_google_sheets()
    sheet.append_row([text])