from petfinder.utils.bot import PetAppBot
from petfinder.utils.database import PetDB
import pathlib


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
    dog_url = "/adopter/?q=e6fec24041f04a949c3897f522576a11_652c4af8b86f4a92be420984a04edf4c#cnt"
    cat_url = "/adopter/?q=e6fec24041f04a949c3897f522576a11_f433d6f7869844e2b86ed4d89d3b05ca#cnt"

    pet_database = PetDB(db_path)
    mybot = PetAppBot(website, pet_database, cred_file)
    mybot.fetch_url_data(dog_url)
    mybot.parse_items('dog')
    mybot.fetch_url_data(cat_url)
    mybot.parse_items('cat')


if __name__ == '__main__':
    main()
