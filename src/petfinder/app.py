""" Main file to instantiate the bot and database and monitor for new postings every 10 minutes"""
import pathlib
import time
from petfinder.bot import WebpageMonitor
from petfinder.database import PetDB

# to do
# switch to PostgreSQL database? could be running in its own container


def main():
    # database file
    delta_t = 600
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
    # simple time spacing between url request call
    while True:
        try:
            for pet_type, pet_url in pet_urls.items():
                bot = WebpageMonitor(website, pet_type, pet_database,
                                     cred_file)
                bot.fetch_url_data(pet_url)
                bot.parse_items()
                bot.detect_new_postings()

            time.sleep(delta_t)
        except RuntimeError:
            print(f"Error running, retrying in {delta_t} seconds.")


if __name__ == '__main__':
    main()
