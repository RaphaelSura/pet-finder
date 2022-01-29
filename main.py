from utils.bot import PetAppBot

# TODO add telegram setup instruction
# TODO github action
# TODO crontab on server (Raspberry PI or HEROKU)


def main():
    # database file
    db_name = "data/dyrevaernet.db"

    # telegram bot credentials
    cred_file = "etc/telegram_creds.txt"

    # url and filters already
    website = "https://dyrevaernet.dk"
    dog_url = "/adopter/?q=e6fec24041f04a949c3897f522576a11_652c4af8b86f4a92be420984a04edf4c#cnt"
    cat_url = "/adopter/?q=e6fec24041f04a949c3897f522576a11_f433d6f7869844e2b86ed4d89d3b05ca#cnt"

    mybot = PetAppBot(website, db_name, cred_file)
    mybot.fetch_data_on_page(dog_url, 'dog')
    mybot.fetch_data_on_page(cat_url, 'cat')


if __name__ == '__main__':
    main()
