import gspread
import time
import os
from dotenv import load_dotenv

load_dotenv()

SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")

client = gspread.auth.service_account(filename='credentials.json')
spreadsheet = client.open_by_url(SPREADSHEET_URL)

def detect_range(data: list, row: int = 1) -> str:
    col_start = 'A'
    col_end = chr(ord(col_start) + len(data) - 1)
    return f"{col_start}{row}:{col_end}{row}"


def backup_data(data:dict):
    today_date = time.strftime("%d-%m-%Y", time.localtime(time.time()))
    data = list(data.values())
    data = [str(i) for i in data]
    try:
        worksheet = spreadsheet.worksheet(today_date)
    except gspread.WorksheetNotFound:
        spreadsheet.add_worksheet(title=today_date, rows=100, cols=20)
        worksheet = spreadsheet.worksheet(today_date)
        range_cols = detect_range(data, 1)
        worksheet.format(range_cols, {'textFormat': {'bold': True}})
    
    worksheet.append_row(data)
    