import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

def get_sheets_client():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    service_account_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')
    if not service_account_file or not os.path.exists(service_account_file):
        print("Google Service Account file not found.")
        return None
    
    credentials = Credentials.from_service_account_file(service_account_file, scopes=scopes)
    client = gspread.authorize(credentials)
    return client

def update_google_sheet(data_rows, sheet_name="Rauly Reports"):
    client = get_sheets_client()
    if not client:
        return
    
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    try:
        sh = client.open_by_key(sheet_id)
        try:
            worksheet = sh.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sh.add_worksheet(title=sheet_name, rows="100", cols="20")
            # Set Headers
            headers = ["Type", "Group/Project", "User/Admin", "Role", "Patterns Found", "Timestamp"]
            worksheet.append_row(headers)
        
        worksheet.append_rows(data_rows)
        print(f"Successfully updated sheet: {sheet_name}")
    except Exception as e:
        print(f"Error updating Google Sheet: {e}")
