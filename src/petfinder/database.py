import sqlite3
import pandas as pd


class PetDB:

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.create()

    def create(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS pet
        (id INTEGER PRIMARY KEY,
        name TEXT,
        age TEXT,
        type_id INTEGER REFERENCES type(id),
        race_id INTEGER REFERENCES race(id),
        teaser TEXT,
        url TEXT NOT NULL UNIQUE,
        creation TIMESTAMP,
        status_id INTEGER REFERENCES status(id))
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS race
        (id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE)
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS type
        (id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE)
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS status
        (id INTEGER PRIMARY KEY,
        value TEXT NOT NULL UNIQUE)
        """)

        # add dog and cat to type table
        if pd.read_sql("SELECT * FROM type", con=self.conn).empty:
            self.cur.execute("INSERT INTO type VALUES (NULL,?)", ('dog', ))
            self.cur.execute("INSERT INTO type VALUES (NULL,?)", ('cat', ))

        # add active (1) and inactive (2) to status table
        if pd.read_sql("SELECT * FROM status", con=self.conn).empty:
            self.cur.execute("INSERT INTO status VALUES (NULL,?)",
                             ('active', ))
            self.cur.execute("INSERT INTO status VALUES (NULL,?)",
                             ('inactive', ))

        self.conn.commit()

    def insert_pet(self, args):
        name, age, pet_type, race, teaser, link_url, date, status_id = args

        # convert race -> race_id
        race_id = self.cur.execute(
            f"SELECT id FROM race WHERE name = '{race}'").fetchone()
        if not race_id:
            self.insert_race(race)
            race_id = self.cur.execute(
                f"SELECT id FROM race WHERE name = '{race}'").fetchone()

        # convert pet_type -> type_id
        type_id = self.cur.execute(
            f"SELECT id FROM type WHERE name = '{pet_type}'").fetchone()

        data = (name, age, type_id[0], race_id[0], teaser, link_url, date,
                status_id)
        self.cur.execute("INSERT INTO pet VALUES (NULL,?,?,?,?,?,?,?,?)", data)
        self.conn.commit()

    def insert_race(self, race):
        self.cur.execute("INSERT INTO race VALUES (NULL,?)", (race, ))
        self.conn.commit()

    def update_status(self, active_ids):
        pass
        # self.cur.execute(
        #     f"""UPDATE INTO pet VALUES (NULL,?)
        # WHERE id NOT IN {active_ids}""", (2, ))
        # self.conn.commit()

    # method to destroy the object: is run when the script is exited
    def __del__(self):
        self.conn.close()
