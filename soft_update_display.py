from datetime import datetime, timedelta
from papirus import PapirusComposite

def soft_update_display(time_since_last_update: datetime, content: PapirusComposite) -> datetime:
    """Write a composite image to the display if it has been at least 0.5 seconds since time_since_last_update."""

    # if the time between time_since_last_update and now is less than 0.5 seconds, just exit the function
    if (datetime.now() - time_since_last_update) < timedelta(milliseconds=500):
        return time_since_last_update
    
    # otherwise, update the display
    # and return the current time
    content.writeAll()
    return datetime.now()
    