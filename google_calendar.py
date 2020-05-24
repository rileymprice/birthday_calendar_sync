from credential_helper import calendar_creds
import json
import sqlite3
from calendar_db import calendar_db
import os

calendar_db = calendar_db()
calendar_service = calendar_creds()

CONTACT_CALENDAR_ID = os.environ.get("CONTACT_CALENDAR")
BIRTHDAY_CALENDAR_ID = os.environ.get("BIRTHDAY_CALENDAR")


def update_birthdays():
    null_data = calendar_db.get_null_birthdays()
    for null_row in null_data:
        date = null_row['date']
        id = null_row['id']
        event_name = null_row['summary']
        event_data = {'summary':event_name,'description':event_name,'start':{'date':date},'recurrence':['RRULE:FREQ=YEARLY;COUNT=5']}
        result = calendar_service.events().insert(calendarId=BIRTHDAY_CALENDAR_ID,body=event_data).execute()


def get_contact_events():
    events = calendar_service.events().list(calendarId=CONTACT_CALENDAR_ID).execute()
    for event in events["items"]:
        event_id = event["id"]
        event_date = event["start"]["date"]
        event_name = event["summary"]
        event_gadget = event["gadget"]["preferences"]
        event_type = event_gadget["goo.contactsEventType"]
        full_name = event_gadget["goo.contactsFullName"]
        if not calendar_db.does_contact_exist(event_id):
            calendar_db.insert_contact_birthday(event_id, full_name, event_date, event_name, event_type)
        else:

if __name__ == "__main__":
    try:
        all_events = get_contact_events()
    except Exception as error:
        print(f"Error getting contact events: {error}")
    else:
        print(all_events)
