import requests
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup


class PetAppBot:

    def __init__(self, web_url, database, telegram_credentials):
        self.base_url = web_url
        self.telegram_cred_file = telegram_credentials
        self.active_posts = []
        self.page_items = []
        self.database = database

    # split this into several methods
    def fetch_url_data(self, filter_url):
        # define browser options
        url = self.base_url + filter_url
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.page_items = soup.find_all('div', {'class': 'item match'})

    def parse_items(self, pet_type):
        # loop thru each item
        for item in self.page_items:
            # link to posting
            link = item.attrs['onclick']
            link_url = self.base_url + link.split("'")[-2]

            # check if url exists in database
            curr_post_id = self.database.cur.execute(
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
                race_id = self.database.cur.execute(
                    f"SELECT id FROM race WHERE name = '{race}'").fetchone()
                if not race_id:
                    self.database.insert_race(race)
                    race_id = self.database.cur.execute(
                        f"SELECT id FROM race WHERE name = '{race}'").fetchone(
                        )

                # type_id
                type_id = self.database.cur.execute(
                    f"SELECT id FROM type WHERE name = '{pet_type}'").fetchone(
                    )

                # populate database
                data = (name, age, type_id[0], race_id[0], teaser, link_url,
                        date, status_id)
                self.database.insert_pet(data)
                curr_post_id = self.database.cur.execute(
                    f"SELECT id FROM pet WHERE url = '{link_url}'").fetchone()

                # send new post to user
                self.send_telegram((pet_type, name, race, age, link_url))

            # add to the list of active posts
            self.active_posts.append(curr_post_id[0])

        # update status in database - need to work on this
        self.database.update_status(self.active_posts)

    def send_telegram(self, pet_info):
        # format the message:
        msg = "New {} up on Dyreværnet \n\n{} \n{} \n{} \n{}".format(*pet_info)
        # send the telegram
        bot_token, bot_chatID = np.loadtxt(self.telegram_cred_file, dtype=str)
        send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={msg}'
        _ = requests.get(send_text)
