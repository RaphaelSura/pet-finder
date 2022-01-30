# pet-finder
App that scrapes the Danish animal protection association website and sends a telegram when a new pet is available. 
Small sized projects that samples a lot of practical code, which can easily be transferrable to other projects:
- Web monitoring/scraping
- SQLite database
- Telegram bot
- Github action
- Crontab

I use this code as a running project to implement newly learned coding techniques and ideas.

## Installation
Regular installation with git. 
```
$ git clone https://github.com/RaphaelSura/pet-finder.git
$ cd pet-finder
$ python -m virtualenv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

## Code formatting
Following Google Python style guide: https://google.github.io/styleguide/pyguide.html. 
Before pushing code to Github, format the code using the following
```
$ yapf *.py -r -i
```

## Telegram bot setup
Install Telegram app on your phone or computer and create an account. Search for Botfather and type the following two commands in the chat:

- ```/start``` to get the BotFather bot setup.

- ```/newbot``` to create a new bot.

Choose a **bot name** e.g. FindMyPetBot. Then choose a **bot usernmae** e.g. mypetfinder_bot (must end with the word 'bot'). After creating the bot, it will display an **HTTP API token**.

In a browser, type https://api.telegram.org/{my_bot_http_api_token}/getUpdates, where you use the correct value for your bot API token. In the response, note down the **Chat ID**. 

Put the **HTTP API token** and **chat ID** into etc/telegram_creds.txt. Note: the *etc* folder is in *.gitignore* as the content shouldn't be public.

## CRONTAB on server (Heroku, Raspberry PI)
```
# python script for Pet App bot, runs avery 10 minutes from 6am til midnight
*/10 6-23 * * * .env/bin/python3 /media/usb1/PythonProjects/pet-finder/main.py
```
