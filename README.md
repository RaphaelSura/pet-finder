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
Install Telegram app on your phone or computer
...

## CRONTAB on Raspberry PI server
```
# python script for Pet App bot, runs avery 10 minutes from 6am til midnight
*/10 6-23 * * * .env/bin/python3 /media/usb1/PythonProjects/pet-finder/main.py
```
