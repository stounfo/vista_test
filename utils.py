def reverse_status(status):
    if status == "Deleted":
        return "Done"
    elif status == "Active":
        return "Done"
    else:
        return "Active"