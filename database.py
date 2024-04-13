import sqlite3

class Database:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # create users, venues, and shows tables using SQL create table statements
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS venues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                place TEXT NOT NULL,
                capacity INTEGER NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                rating TEXT NOT NULL,
                tags TEXT NOT NULL,
                ticket_price INTEGER NOT NULL,
                venue_id INTEGER NOT NULL,
                FOREIGN KEY (venue_id) REFERENCES venues(id)
            )
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()

    # add methods to interact with the database (e.g., insert, update, delete, select)
    # ...
