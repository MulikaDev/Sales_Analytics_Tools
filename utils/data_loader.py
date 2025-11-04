import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def load_data(service_account_file, sheet_name, tab_name):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_file(service_account_file, scopes=scopes)
    gc = gspread.authorize(credentials)
    sheet = gc.open(sheet_name).worksheet(tab_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)
