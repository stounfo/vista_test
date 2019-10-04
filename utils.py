from datetime import datetime



def reverse_status(status):
    if status == "Deleted":
        return "Done"
    elif status == "Active":
        return "Done"
    else:
        return "Active"


def datetime_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
