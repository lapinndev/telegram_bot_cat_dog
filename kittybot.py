# kittybot/kittybot.py

import logging
import os

import requests

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

from dotenv import load_dotenv 

load_dotenv()

secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


URL_CAT = 'https://api.thecatapi.com/v1/images/search'
URL_DOG = 'https://api.thedogapi.com/v1/images/search'


def get_cat_image():
    try:
        response = requests.get(URL_CAT)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

def get_dog_image():
    try:
        response = requests.get(URL_DOG)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thecatapi.com/v1/images/search'
        response = requests.get(new_url)

    response = response.json()
    random_dog = response[0].get('url')
    return random_dog



def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_cat_image())

def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_dog_image())


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = [['/cat'], ['/dog']]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Выбери, какого питомца ты хочешь увидеть'.format(name),
        reply_markup=reply_markup
    )



def main():
    updater = Updater(token=secret_token)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('cat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('dog', new_dog))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()