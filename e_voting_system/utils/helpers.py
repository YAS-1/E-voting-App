import datetime

# the helper functions -> used by the other modules to add application features

def current_timestamp() -> str:
    return str(datetime.datetime.now())