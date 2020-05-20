from credential_helper import calendar_creds
import json
import sqlite3
from calendar_db import calendar_db

calendar_db = calendar_db()
calendar_service = calendar_creds()

birthday_calendar_id = "dhig8c0eiic01g4r895tgpu04o@group.calendar.google.com"
contacts_calendar_id = "addressbook#contacts@group.v.calendar.google.com"


def create_events():
    for event in event_list:
        calendar_service.events().insert(
            calendarId=birthday_calendar_id, body=event
        ).execute()


if __name__ == "__main__":
    try:
        all_events = get_contacts_events()
    except Exception as error:
        print(f"Error getting contact events: {error}")
    else:
        try:
            create_events(all_events)
        except Exception as error:
            print(f"Error creating events: {error}")
