import requests
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


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

        # add dog and cat to type table
        if pd.read_sql("SELECT * FROM status", con=self.conn).empty:
            self.cur.execute("INSERT INTO status VALUES (NULL,?)",
                             ('active', ))
            self.cur.execute("INSERT INTO status VALUES (NULL,?)",
                             ('inactive', ))

        self.conn.commit()

    def insert_pet(self, args):
        self.cur.execute("INSERT INTO pet VALUES (NULL,?,?,?,?,?,?,?,?)", args)
        self.conn.commit()

    def insert_race(self, race):
        self.cur.execute("INSERT INTO race VALUES (NULL,?)", (race, ))
        self.conn.commit()

    # method to destroy the object: is run when the script is exited
    def __del__(self):
        self.conn.close()


class PetAppBot:

    def __init__(self, web_url, db_path, telegram_credentials):
        self.base_url = web_url
        self.telegram_cred_file = telegram_credentials
        self.active_posts = []
        self.db = PetDB(db_path)

    # split this into several methods
    def fetch_data_on_page(self, filter_url, pet_type):
        # define browser options
        url = self.base_url + filter_url
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # loop thru each item
        for item in soup.find_all('div', {'class': 'item match'}):
            # link to posting
            link = item.attrs['onclick']
            link_url = self.base_url + link.split("'")[-2]

            # check if url exists in db
            curr_post_id = self.db.cur.execute(
                f"SELECT id FROM pet WHERE url = '{link_url}'").fetchone()
            if not curr_post_id:
                # posting info
                name = item.find('h3').text
                if pet_type == 'cat' and 'inde' not in name:
                    continue
                race = item.find('div', {'class': 'race'}).text
                race = race.replace("Race: ", "")
                age = item.find('div', {'class': 'age'}).text
                age = age.replace("Alder: ", "")
                teaser = item.find('div', {'class': 'teaser'}).text
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                status_id = 1
                if len(teaser) > 100:
                    teaser = teaser[:100] + '...'

                # check race from table race
                race_id = self.db.cur.execute(
                    f"SELECT id FROM race WHERE name = '{race}'").fetchone()
                if not race_id:
                    self.db.insert_race(race)
                    race_id = self.db.cur.execute(
                        f"SELECT id FROM race WHERE name = '{race}'").fetchone(
                        )

                # type_id
                type_id = self.db.cur.execute(
                    f"SELECT id FROM type WHERE name = '{pet_type}'").fetchone(
                    )

                # populate database
                data = (name, age, type_id[0], race_id[0], teaser, link_url,
                        date, status_id)
                self.db.insert_pet(data)
                curr_post_id = self.db.cur.execute(
                    f"SELECT id FROM pet WHERE url = '{link_url}'").fetchone()

                # send new post to user
                self.send_telegram((pet_type, name, race, age, link_url))

            # add to the list of active posts
            self.active_posts.append(curr_post_id[0])

        # TODO
        # self.db.update_status(self.active_posts)

    def send_telegram(self, pet_info):
        # format the message:
        msg = "New {} up on Dyreværnet \n\n{} \n{} \n{} \n{}".format(*pet_info)
        # send the telegram
        bot_token, bot_chatID = np.loadtxt(self.telegram_cred_file, dtype=str)
        send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={msg}'
        _ = requests.get(send_text)
