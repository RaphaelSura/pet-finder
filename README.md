![build](https://github.com/RaphaelSura/pet-finder/actions/workflows/build.yml/badge.svg)

# pet-finder
App that scrapes the Danish animal protection association website and sends a telegram when a new pet is available. 
Small sized projects that samples a lot of practical code, which can easily be transferrable to other projects:
- Web monitoring/scraping
- SQLite database
- Telegram bot
- Github action
- Crontab
- Docker containers

I use this code as a running project to implement newly learned coding techniques and ideas.

## Installation
The repo is setup so as to install ```petfinder``` as a package. Once cloned and done creating a virtual environment, pip install the repo in editable mode (-e), which will take care of all the dependencies.
```
$ git clone https://github.com/RaphaelSura/pet-finder.git
$ cd pet-finder
$ python -m virtualenv .env
$ source .env/bin/activate
$ pip install -e .
```
Now ``` petfinder ``` is like any other python package.
```
from petfinder.database import PetDB
```
## Code formatting
Following Google Python style guide: https://google.github.io/styleguide/pyguide.html. 
This is set in VScode via ``` .vscode/settings.json ```. Alternatively, run manually:
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

## Run the app - several ways
### CRONTAB on Ubuntu server
```
# python script for Pet App bot, runs every 10 minutes from 6am til midnight
*/10 6-23 * * * ~/pet-finder/.env/bin/python3 ~/pet-finder/app_with_crontab.py
```
### Inside DOCKER container
```
cd pet-finder
docker build -t pet-finder:latest .
```
Get the image_id with ``` docker images | grep pet-finder ```. Then run in detached mode:
```
docker run -d --restart unless-stopped image_id
```
