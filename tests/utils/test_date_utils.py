from ragnarok.utils.date_utils import readable_today_date


def test_readable_today_date():
    """
    Test case for `readable_today_date` function.
    """
    result = readable_today_date()
    assert isinstance(result, str)
    assert len(result) > 0
