import sqlite3
from LogHelp import logger

logger = logger(__name__)


class calendar_db:
    def __init__(self):
        self.conn = sqlite3.connect("calendar.db")
        self.cur = self.conn.cursor()
        self.conn.row_factory = dict_factory
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS contact_event (id TEXT PRIMARY KEY,full_name TEXT,date DATE,event_name TEXT)"
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS birthday_event (id TEXT PRIMARY KEY,event_name TEXT,contact_event_id TEXT REFERENCES contact_event (id),date DATE)"
        )
        self.conn.commit()

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def insert_contact_birthday(self, id, full_name, date, event_name):
        try:
            logger.info("Inserting contact birthday")
            self.cur.execute(
                "INSERT INTO contact_event (id,full_name,date,event_name) VALUES (?,?,?,?)",
                (id, full_name, date, event_name),
            )
        except sqlite3.IntegrityError as error:
            logger.error(f"Error inserting contact birthday: {error}")
        else:
            logger.info(f"Inserted {id} into contact_event")
            self.conn.commit()

    def insert_birthday_event(self, id, name, contact_event_id, date):
        try:
            logger.info(f"Iserting {name} and {date} into birthday_event")
            self.cur.execute(
                "INSERT INTO birthday_event (id,name,contact_event_id,date) VALUES (?,?,?,?)",
                (id, name, contact_event_id, date),
            )
        except sqlite3.IntegrityError as error:
            logger.error(f"Error inserting birthday event: {error}")
        else:
            logger.info(f"Inserted {name} and {date} into birthday_event")
            self.conn.commit()

    def get_columns(self, table):
        sql = f"PRAGMA table_info({table})"
        columns = self.cur.execute(sql)
        all_columns = columns.fetchall()
        column_names = all_columns.keys()
        return column_names

    def get_birthday_events(self):
        try:
            events = self.cur.execute("SELECT * FROM birthday_event")
        except sqlite3.Error as error:
            logger.Error(f"Error getting birthday events: {error}")
        else:
            all_events = events.fetchall()
            return all_events

    def get_contact_birthdays(self):
        events = self.cur.execute("SELECT * FROM contact_event")
        all_events = events.fetchall()
        return all_events
