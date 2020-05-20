import sqlite3

sql = """INSERT INTO contact_event (
                              id,
                              name,
                              date
                          )
                          VALUES (
                              '3',
                              'george',
                              '1990-12-03'
                          );
"""

db_conn = sqlite3.connect("calendar.db")
db_curr = db_conn.cursor()

db_curr.execute(sql)
