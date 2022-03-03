""" Main file to instantiate the bot and database and monitor for new postings
    Only runs once. Can be setup in crontab to run on regular basis."""

import pathlib
from petfinder.bot import WebpageMonitor
from petfinder.database import PetDB


def main():
    """
    # the app is run through crontab and is started every 10 minutes
    $ crontab -e
    */10 6-23 * * * /usr/bin/python3 /path-to-folder/pet-finder/app_with_crontab.py
    """
    # database file
    project_dir = pathlib.Path(__file__).parent.parent.parent.resolve()
    db_path = project_dir.joinpath("data", "dyrevaernet.db")
    # telegram bot credentials
    cred_file = project_dir.joinpath("etc", "telegram_creds.txt")

    # url and filters already
    website = "https://dyrevaernet.dk"
    pet_urls = {
        'dog':
        "/adopter/?q=e6fec24041f04a949c3897f522576a11_652c4af8b86f4a92be420984a04edf4c#cnt",
        'cat':
        "/adopter/?q=e6fec24041f04a949c3897f522576a11_f433d6f7869844e2b86ed4d89d3b05ca#cnt"
    }

    pet_database = PetDB(db_path)
    for pet_type, pet_url in pet_urls.items():
        bot = WebpageMonitor(website, pet_type, pet_database, cred_file)
        bot.fetch_url_data(pet_url)
        bot.parse_items()
        bot.detect_new_postings()


if __name__ == '__main__':
    main()
