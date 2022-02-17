import time
import pathlib
from petfinder.bot import PetAppBot
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
    dog_url = "/adopter/?q=e6fec24041f04a949c3897f522576a11_652c4af8b86f4a92be420984a04edf4c#cnt"
    cat_url = "/adopter/?q=e6fec24041f04a949c3897f522576a11_f433d6f7869844e2b86ed4d89d3b05ca#cnt"

    # start the bot - once
    pet_database = PetDB(db_path)
    mybot = PetAppBot(website, pet_database, cred_file)

    # simple time spacing between url request call
    while True:
        try:
            mybot.fetch_url_data(dog_url)
            mybot.parse_items('dog')
            mybot.fetch_url_data(cat_url)
            mybot.parse_items('cat')
            time.sleep(delta_t)
        except RuntimeError:
            print(f"Error running, retrying in {delta_t} seconds.")


if __name__ == '__main__':
    main()
