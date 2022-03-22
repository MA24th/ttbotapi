import os

import ttbotapi
import logging

ttbotapi.logger.setLevel(logging.DEBUG)

bot = ttbotapi.Bot(access_token=os.getenv('access_token'))


@bot.update_handler(chat_type='dialog', bot_command=['/start', '/help'])
def send_welcome(update):
    bot.send_message(text="Howdy, how are you doing?", user_id=update.message.sender.user_id, chat_id=None,
                     link={'type': 'reply', 'mid': update.message.body.mid})


@bot.update_handler(chat_type='dialog', regexp='hi')
def send_hi(update):
    bot.send_message(text=f'Hi 👋, {update.message.sender.name}', user_id=update.message.sender.user_id, chat_id=None)


@bot.update_handler(func=lambda update: update.message.body.text)
def echo(update):
    bot.send_message(text=update.message.body.text, user_id=update.message.sender.user_id, chat_id=None)


bot.polling()
