import sqlite3
from LogHelp import logger

logger = logger(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class calendar_db:
    def __init__(self):
        self.conn = sqlite3.connect("calendar.db")
        self.cur = self.conn.cursor()
        self.conn.row_factory = dict_factory
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT,full_name TEXT,date DATE,event_name TEXT,event_type TEXT,contact_event_id TEXT,birthday_event_id TEXT)"
        )
        self.conn.commit()

    def insert_contact_birthday(
        self, contact_event_id, full_name, date, event_name, event_type
    ):
        try:
            logger.info("Inserting contact birthday")
            self.cur.execute(
                "INSERT INTO events (full_name,date,event_name,event_type,contact_event_id) VALUES (?,?,?,?,?)",
                (full_name, date, event_name, event_type, contact_event_id),
            )
        except sqlite3.IntegrityError as error:
            logger.error(f"Error inserting contact birthday: {error}")
        else:
            logger.info(f"Inserted {contact_event_id} into events")
            self.conn.commit()

    def update_birthday_id(self, id, birthday_event_id):
        try:
            logger.info(f"Updating birthday event id for id: {id}")
            self.cur.execute(
                "UPDATE events SET birthday_event_id=? WHERE id=?",
                (birthday_event_id, id),
            )
        except sqlite3.Error as error:
            logger.error(f"Error updating birthday_event_id for {id}: {error}")
        else:
            logger.info(f"Updated birthday_event_id for {id}")
            self.conn.commit()

    def get_null_birthdays(self):
        try:
            logger.info("Getting Null birthday ids")
            null_birthday_data = self.cur.execute(
                "SELECT * FROM events WHERE birthday_event_id is null"
            )
        except sqlite3.Error as error:
            logger.error(f"Error getting null birthday data: {error}")
        else:
            null_data = null_birthday_data.fetchall()
            return null_data

    def does_contact_exist(self, contact_event_id):
        try:
            logger.info(f"Checking if contact_event_id exists: {contact_event_id}")
            data = self.cur.execute(
                "SELECT * FROM events WHERE contact_event_id=?", (contact_event_id,)
            )
        except sqlite3.Error as error:
            logger.error(f"Error checking contact id {contact_event_id}:{error}")
        else:
            rows = data.fetchall()
            if len(rows) > 0:
                return True
            else:
                return False

    def get_event(self, contact_event_id):
        try:
            logger.info(f"Getting birthday for contact_ID {contact_event_id}")
            data = self.cur.execute(
                "SELECT * FROM events WHERE contact_event_id=?", (contact_event_id,)
            )
        except sqlite3.Error as error:
            logger.error(
                f"Error getting event for contact_id {contact_event_id}: {error}"
            )
        else:
            return data


if __name__ == "__main__":
    cal = calendar_db()
    print(cal.get_null_birthday_ids())
