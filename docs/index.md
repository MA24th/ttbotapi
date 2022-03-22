# ttbotapi
[TamTam Bot API](https://dev.tamtam.chat) library

[![GPLv2 license](https://img.shields.io/badge/LICENSE-GPLv2-red)](https://github.com/ma24th/ttbotapi/blob/master/LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-v0.3.0-yellow.svg)](https://pypi.org/project/ttbotapi/)
[![Python package](https://github.com/MA24th/ttbotapi/workflows/Python%20package/badge.svg)](https://github.com/MA24th/ttbotapi/actions/workflows/python-package.yml)
[![Upload Python Package](https://github.com/MA24th/ttbotapi/workflows/Upload%20Python%20Package/badge.svg)](https://github.com/MA24th/ttbotapi/actions/workflows/python-publish.yml)

## How to Use
### Installation
There are two ways to install the framework:
* Installation using Python package manager:
```bash
$ pip install ttbotapi
```
* Installation from source (requires git):

```bash
$ git clone https://github.com/ma24th/ttbotapi.git
$ cd ttbotapi
$ python setup.py install
```

### Guide
The Bot class encapsulates all API calls in a single class. It provides functions such as 
`send_xyz` (`send_message`, `edit_message` etc.) and several ways to listen for incoming messages.

Create a file called `echo_bot.py`.
Then, open the file and create an instance of the Bot class.
```python
import ttbotapi
import logging

ttbotapi.logger.setLevel(logging.DEBUG)

# Note: Make sure to actually replace TOKEN with your own API token.
bot = ttbotapi.Bot(access_token='Bot Token')

# After that declaration, we need to register some so-called decorator handlers.
# Update handlers define filters which a message must pass. If a message passes the filter, 
# the decorated function is called and the incoming message is passed as an argument.

# Let's define a message handler which handles incoming `/start` and `/help` bot_command in dialog chat type.
@bot.update_handler(chat_type='dialog', bot_command=['/start', '/help'])
def send_welcome(update):
    # A function which is decorated by an update handler can have an arbitrary name, 
    # however, it must have only one parameter (the update)
    bot.send_message(text="Howdy, how are you doing?", user_id=update.message.sender.user_id, chat_id=None,
                     link={'type': 'reply', 'mid': update.message.body.mid})

# Let's add another handler
@bot.update_handler(chat_type='dialog', regexp='hi')
def send_hi(update):
    bot.send_message(text=f'Hi 👋, {update.message.sender.name}', user_id=update.message.sender.user_id, chat_id=None)


# This one echoes all incoming text messages back to the sender. It uses a lambda function to test a message. 
# If the lambda returns True, the message is handled by the decorated function. 
# Since we want all messages to be handled by this function, we simply always return True.
@bot.update_handler(func=lambda update: update.message.body.text)
def echo(update):
    bot.send_message(text=update.message.body.text, user_id=update.message.sender.user_id, chat_id=None)


# Using long polling now our bot never stop working
bot.polling()

# Alright, that's it! Our source file now looks fine
```
To start the bot, simply open up a terminal and enter `python echo_bot.py` to run the bot! 
Test it by sending commands ('/start' and '/help') and arbitrary text messages.


## How to Contribute
- You must follow [Contributing](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/CONTRIBUTING.md) Guidelines.
- We are committed to providing a friendly community, for more experience read [Code Of Conduct](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/CODE_OF_CONDUCT.md).


## How to Communicate
You're welcome to drop in and ask questions, 
discuss bugs and such, Check [Communication](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/COMMUNICATION.md) Methods.


## Frequently Asked Questions
- Please ask


## Attribution
These Documents are adapted for [MA24th Open Source Software](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/),
For more information [contact me](mailto:ma24th@yahoo.com) with any additional questions or comments.


## Support
Join our channel on [![TamTam Channel](https://img.shields.io/badge/TamTam-Channel-blue.svg)](https://tt.me/ttbotapic)
and [![Discord Server](https://img.shields.io/badge/Discord-Server-blue.svg)](https://discord.gg/g65AqbPK6g) .