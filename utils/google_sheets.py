import gspread
from google.oauth2.service_account import Credentials
import logging

def update_google_sheet(df, sheet_url, worksheet_name, service_account_file):
    logging.info(f"🔄 Updating Google Sheet: {worksheet_name}...")
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
    client = gspread.authorize(creds)

    sheet = client.open_by_url(sheet_url)
    try:
        worksheet = sheet.worksheet(worksheet_name)
        worksheet.clear()
    except gspread.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    logging.info("✅ Google Sheet updated successfully!")
