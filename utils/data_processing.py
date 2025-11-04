import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_data_from_gsheet(sheet_url, worksheet_name, service_account_file):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(service_account_file, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_url(sheet_url).worksheet(worksheet_name)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df

def prepare_summary(df):
    # Розрахунок total_sales, total_profit, avg_profit_margin
    df['total_sales'] = df['units_sold'] * df['unit_price']
    df['total_profit'] = df['units_sold'] * (df['unit_price'] - df['cost_per_unit'])
    df['avg_profit_margin'] = df['total_profit'] / df['total_sales'] * 100

    # Групування по продукту
    df_summary = df.groupby('product', as_index=False).agg({
        'units_sold': 'sum',
        'total_sales': 'sum',
        'total_profit': 'sum',
        'unit_price': 'mean',
        'cost_per_unit': 'mean',
        'avg_profit_margin': 'mean'
    })

    # Форматування валюти та %
    df_summary['unit_price'] = df_summary['unit_price'].apply(lambda x: f"${x:,.2f}")
    df_summary['cost_per_unit'] = df_summary['cost_per_unit'].apply(lambda x: f"${x:,.2f}")
    df_summary['total_sales'] = df_summary['total_sales'].apply(lambda x: f"${x:,.2f}")
    df_summary['total_profit'] = df_summary['total_profit'].apply(lambda x: f"${x:,.2f}")
    df_summary['avg_profit_margin'] = df_summary['avg_profit_margin'].apply(lambda x: f"{x:.1f}%")

    return df_summary

