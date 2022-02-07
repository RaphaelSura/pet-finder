from utils.bot import PetAppBot
import pathlib

# TODO add telegram setup instruction
# TODO github action
# TODO crontab on server (Raspberry PI or HEROKU)


def main():
    # database file
    project_dir = pathlib.Path(__file__).parent.resolve()
    db_path = project_dir.joinpath("data", "dyrevaernet.db")

    # telegram bot credentials
    cred_file = project_dir.joinpath("etc", "telegram_creds.txt")

    # url and filters already
    website = "https://dyrevaernet.dk"
    dog_url = "/adopter/?q=e6fec24041f04a949c3897f522576a11_652c4af8b86f4a92be420984a04edf4c#cnt"
    cat_url = "/adopter/?q=e6fec24041f04a949c3897f522576a11_f433d6f7869844e2b86ed4d89d3b05ca#cnt"

    mybot = PetAppBot(website, db_path, cred_file)
    mybot.fetch_data_on_page(dog_url, 'dog')
    mybot.fetch_data_on_page(cat_url, 'cat')


if __name__ == '__main__':
    main()
