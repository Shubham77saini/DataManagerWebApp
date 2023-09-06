from datetime import datetime, timedelta


# This function will extract the date_only from timestamp.
def converts_timestamp_to_date_only(each_dict):
    timestamp = each_dict["date"]
    datetime_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
    date_only = str(datetime_obj.date())
    return date_only
