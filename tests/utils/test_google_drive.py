from unittest.mock import patch, Mock
import pandas as pd

from src.utils.google_drive import download_google_sheet


@patch("src.utils.google_drive.gspread.service_account")
def test_download_google_sheet_as_dataframe(mock_service_account):
    mock_gc = Mock()
    mock_service_account.return_value = mock_gc
    mock_sheet = Mock()
    mock_gc.open_by_key.return_value = mock_sheet
    mock_worksheet = Mock()
    mock_sheet.get_worksheet.return_value = mock_worksheet
    mock_worksheet.get_all_records.return_value = [{"Name": "John Doe", "Age": 30}]

    result = download_google_sheet("fake_sheet_id", 0, as_pandas=True)
    assert isinstance(result, pd.DataFrame)
    assert result.to_dict("records") == [{"Name": "John Doe", "Age": 30}]


@patch("src.utils.google_drive.gspread.service_account")
def test_download_google_sheet_as_list(mock_service_account):
    mock_gc = Mock()
    mock_service_account.return_value = mock_gc
    mock_sheet = Mock()
    mock_gc.open_by_key.return_value = mock_sheet
    mock_worksheet = Mock()
    mock_sheet.get_worksheet.return_value = mock_worksheet
    mock_worksheet.get_all_records.return_value = [{"Name": "Jane Doe", "Age": 25}]

    result = download_google_sheet("fake_sheet_id", 0, as_pandas=False)
    assert result == [{"Name": "Jane Doe", "Age": 25}]
