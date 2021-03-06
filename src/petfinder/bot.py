""" File where the main bot is defined: class WebpageMonitor"""
from datetime import datetime
from pathlib import Path
import numpy as np
import requests
from bs4 import BeautifulSoup
from petfinder.database import PetDB


class WebpageMonitor:
    """ Main class fetching data on website, communicating with database and sending telegram """

    def __init__(self, website: str, pet_type: str, database: PetDB,
                 telegram_info: Path):
        self.website = website
        self.pet_type = pet_type
        self.active_postings = {}
        self.page_items = []
        self.database = database

        # additional filter based on pet_type - string that should be in name
        self.filter = {'dog': '', 'cat': 'inde'}

        # credentials for sending telegram
        self.token, self.chat_id = np.loadtxt(telegram_info, dtype=str)

    def fetch_url_data(self, specific_url):
        # define browser options
        url = self.website + specific_url
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.page_items = soup.find_all('div', {'class': 'item match'})

    def parse_items(self):
        # loop thru each item and store in a dict(url: data)
        for item in self.page_items:
            # link to posting
            link = item.attrs['onclick']
            link_url = self.website + link.split("'")[-2]

            # posting info
            name = item.find('h3').text
            race = item.find('div', {'class': 'race'}).text
            race = race.replace("Race: ", "")
            age = item.find('div', {'class': 'age'}).text
            age = age.replace("Alder: ", "")
            teaser = item.find('div', {'class': 'teaser'}).text
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status_id = 1
            if len(teaser) > 100:
                teaser = teaser[:100] + '...'

            # aggregate data
            data = (name, age, self.pet_type, race, teaser, link_url, date,
                    status_id)

            # add to the list of active posts
            if self.filter[self.pet_type] in name:
                self.active_postings[link_url] = data

    def detect_new_postings(self):
        for url, data in self.active_postings.items():
            # returns id if exists else None
            curr_post_id = self.database.cur.execute(
                f"SELECT id FROM pet WHERE url = '{url}'").fetchone()
            # if empty -> new data -> add to database
            if not curr_post_id:
                self.database.insert_pet(data)
                useful_data = (self.pet_type, data[0], data[3], data[1], url)
                self.notify_user(useful_data)

        # update status in database - need to work on this
        # status is 2 (inactive) for all, then set 1 (active) for all postings
        # self.database.update_status(self.active_posts)

    def notify_user(self, pet_info):
        # format the message:
        pet_emoji = {'dog': '????', 'cat': '????'}
        pet_type, name, race, age, url = pet_info
        msg = f"New {pet_emoji[pet_type]} up on Dyrev??rnet. \n\n{name}\n{race}\n{age}\n{url}"
        # send the telegram
        send_text = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&parse_mode=Markdown&text={msg}"
        requests.get(send_text)
