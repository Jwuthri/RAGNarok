import gspread
import pandas as pd


def download_google_sheet(google_sheet_id: str, worksheet_id: int, as_pandas: bool = True) -> pd.DataFrame:
    gc = gspread.service_account()
    sheet = gc.open_by_key(google_sheet_id)
    worksheet = sheet.get_worksheet(worksheet_id)
    records = worksheet.get_all_records()
    if as_pandas:
        return pd.DataFrame(records)

    return records
