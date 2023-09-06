from datetime import datetime, timedelta


def validate_date_within_past_year(cls, val):
    current_date = datetime.now().date()
    min_date = current_date - timedelta(days=365)
    max_date = current_date
    timestamp = val["date"]
    datetime_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
    date_only = str(datetime_obj.date())
    date_obj = datetime.strptime(date_only, "%Y-%m-%d").date()
    if date_obj and min_date <= date_obj <= max_date:
        pass
    else:
        raise ValueError(
            "Invalid date. Please check the date should be within the past year from the current date or check the format YYYY-MM-DD (e.g., 2023-05-16)"
        )

    return val
